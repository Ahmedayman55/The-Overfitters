"""Safety layer. Runs on three things, before any model sees them or any text leaves:

1. screen_brief(): the founder's idea. Excluded products are refused
   (physical goods; financial, investment or crypto; health or legal advice).
2. screen_request(): any free-text instruction (dashboard "Ask the team" box,
   CLI, agent tasks). Refuses fake reviews/testimonials/sign-ups, fake urgency,
   income promises, impersonation, moving money, storing credentials,
   paywalling core features, spam and skipping founder approval.
3. scan_output(): everything an agent writes. Sentences that promise income,
   fake urgency or social proof, or invent testimonials are removed before
   the text is saved or shown.

The rules are deterministic on purpose: they cannot be talked out of their
job by a clever prompt, and they are covered by tests/test_guardrails.py and
the trick prompts in evals/trick_prompts.json.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

FLAGS = re.IGNORECASE | re.UNICODE


@dataclass
class Verdict:
    allowed: bool
    category: str | None = None
    reason: str = ""
    safe_alternative: str = ""
    matches: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {"allowed": self.allowed, "category": self.category, "reason": self.reason,
                "safe_alternative": self.safe_alternative, "matches": self.matches}


def _rx(*patterns: str) -> list[re.Pattern]:
    return [re.compile(p, FLAGS) for p in patterns]


# ---------------------------------------------------------------- 1. briefs
EXCLUDED_PRODUCTS: dict[str, dict] = {
    "physical_goods": {
        "reason": "Physical goods are out of scope: this system only builds digital products.",
        "patterns": _rx(
            r"\b(t-?shirts?|hoodies?|mugs?|merch(andise)?|clothing|apparel|jewel(le)?ry|furniture|candles?|soap|cosmetics?|"
            r"skincare|handmade|dropship(ping)?|print[- ]on[- ]demand|physical (product|goods|book|copies)|shipping|"
            r"warehouse|inventory|snack boxes|bakery|coffee beans|meal kits|sneakers|shoes|bags|toys?|gadgets?|devices?|hardware|"
            r"3d[- ]printed|stickers?|posters? shipped|printed (planners?|books?|copies|notebooks?|cards?)|shipped|ships? to|ship(ping)? (it|them|to))\b",
            r"(منتجات? ملموسة|ملابس|تيشيرت|اكسسوارات|شحن)"),
    },
    "financial": {
        "reason": "Financial, investment and crypto products are excluded.",
        "patterns": _rx(
            r"\b(crypto(currency|currencies)?|bitcoin|btc|ethereum|nft|token sale|ico|defi|forex|fx signals|"
            r"trading (signals?|bot|course|strategy|alerts?)|stock (picks?|tips|signals)|day[- ]?trading|investment (advice|fund|plan|course|signals?)|"
            r"invest(ing)? (tips|advice|signals)|portfolio management|loans?|lending|credit repair|insurance|"
            r"tax advice|wealth management|financial advi(c|s)e|get rich|money[- ]making (scheme|system))\b",
            r"(عملات? رقمية|كريبتو|بيتكوين|تداول|توصيات (اسهم|أسهم)|استثمار|قروض)"),
    },
    "health": {
        "reason": "Health and medical advice products are excluded.",
        "patterns": _rx(
            r"\b(medical|medicine|diagnos(is|e|tic)|symptoms?|treatment|cure|therapy|therapist|mental health (treatment|advice|app)|"
            r"diet plans?|meal plans? for (weight|diabet)|weight[- ]loss|supplements?|nutrition(al)? (plan|advice)|fitness program|"
            r"workout plan|keto|fasting protocol|health (advice|coaching|plan)|pregnan(cy|t)|medication|dosage|clinical)\b",
            r"(طبي|علاج|تشخيص|أعراض|اعراض|حمية|رجيم|انقاص الوزن|إنقاص الوزن|مكملات)"),
    },
    "legal_advice": {
        "reason": "Legal advice products are excluded.",
        "patterns": _rx(
            r"\b(legal advice|lawyer|attorney|legal (consult|counsel|service)|immigration advice|visa advice|"
            r"contract review service|divorce|lawsuit|court case|legal templates? for clients|will and testament|legal contracts?|contract templates?|drafting contracts? for clients)\b",
            r"(استشارات? قانونية|محامي|قضية|قانوني للعملاء)"),
    },
}


def screen_brief(brief: dict | str) -> Verdict:
    """Refuse a founder brief whose product falls in an excluded category.

    Only the product idea and target market are screened. The founder's
    background (for example "I am a nurse") is not a product.
    """
    if isinstance(brief, dict):
        text = " ".join(str(brief.get(k, "")) for k in ("idea", "product", "target_market", "title"))
    else:
        text = str(brief)
    for category, spec in EXCLUDED_PRODUCTS.items():
        hits = [m.group(0) for p in spec["patterns"] for m in p.finditer(text)]
        if hits:
            return Verdict(False, f"excluded_product:{category}", spec["reason"],
                           "Pick a digital product (a template, guide, toolkit, course, checklist or small software tool) "
                           "outside these categories, and the pipeline will run.", sorted(set(h.lower() for h in hits)))
    return Verdict(True)


# --------------------------------------------------------------- 2. requests
REQUEST_RULES: list[dict] = [
    {
        "category": "fake_reviews",
        "reason": "We never write reviews, ratings or testimonials. Only real buyers can give them.",
        "safe": "I can draft a short, honest email (for you to approve) that asks real buyers for feedback, "
                "and a page section that shows real reviews once they exist.",
        "patterns": _rx(
            r"\b(quotes?|words|stories|praise)\b[^.?!\n]{0,20}\bfrom\b[^.?!\n]{0,15}\b(satisfied|happy|grateful|delighted)?\s*(buyers?|customers?|users?|students?|clients?)\b",
            r"\bsocial proof\b",
            r"\b(tweet|post|message|email|comment|review|dm)\b[^.?!\n]{0,15}\bfrom\b[^.?!\n]{0,10}\b(a |an )?(happy|satisfied|real|grateful|former)\s+(customer|buyer|user|student|client)s?\b",

            r"\b(write|generate|create|make|draft|produce|give me|need|post|add|invent|come up with|fill)\b[^.?!\n]{0,60}"
            r"\b(reviews?|testimonials?|ratings?|endorsements?|customer (quotes|stories|feedback)|success stories|five[- ]star|5[- ]star|5 stars)\b",
            r"\b(fake|made[- ]up|invented|placeholder|sample|dummy|sock ?puppet|astroturf)\b[^.?!\n]{0,30}\b(reviews?|testimonials?|ratings?|customers?|quotes)\b",
            r"\b(reviews?|testimonials?)\b[^.?!\n]{0,40}\b(from|by) (happy|satisfied|real-sounding|different) (customers|users|people)",
            r"\b(pretend|as if)\b[^.?!\n]{0,40}\b(customers?|users?|buyers?)\b[^.?!\n]{0,30}\b(said|love|loved|reviewed)\b",
            r"(تقييمات?|مراجعات?|شهادات? (عملاء|العملاء)|آراء (عملاء|العملاء)|اراء العملاء|خمس نجوم|5 نجوم)",
            r"\b(perspective|point of view|voice|pov|shoes)\b[^.?!\n]{0,10}\bof\b[^.?!\n]{0,25}\b(user|customer|buyer|client|student|reader)s?\b",
        ),
        "exempt": _rx(r"\b(summari[sz]e|analy[sz]e|read through|organi[sz]e)\b[^.?!\n]{0,40}\b(real|my|interview|actual)\b", r"\b(ask|asking|request|requesting|collect|collecting|invite|inviting|gather|encourage)\w*\b[^.?!\n]{0,40}\b(real |honest |genuine )?(buyers?|customers?|users?|reviews?|feedback)\b"),
    },
    {
        "category": "fake_signups_or_metrics",
        "reason": "We never invent sign-ups, users, followers, sales or other numbers. Gates only use real data.",
        "safe": "I can show the real waitlist count (even if it is small) and suggest honest ways to reach more people.",
        "patterns": _rx(
            r"\b\d[\d,]*\+?\s*(\w+\s)?(have |already )?(joined|signed up|bought|purchased|are using|downloaded)\b",

            r"\b(fake|inflate|inflated|pad|padded|boost|made[- ]up|bots?|buy)\b[^.?!\n]{0,40}\b(sign[- ]?ups?|signups|users|followers|subscribers|waitlist|downloads|sales|numbers|metrics|traffic|likes)\b",
            r"\b(say|claim|pretend|tell (them|people)|show)\b[^.?!\n]{0,40}\b\d[\d,]*\+?\s*(people|users|customers|students|founders|sign[- ]?ups|subscribers|buyers)\b",
            r"\b(pretend|claim)\b[^.?!\n]{0,40}\b(we have|we've got|there are)\b",
            r"\b(mark|set|change|record)\b[^.?!\n]{0,30}\b(waitlist|sign[- ]?ups?|gate)\b[^.?!\n]{0,30}\b(to|as) (\d+|passed|go)\b",
            r"(تسجيلات? (وهمية|مزيفة)|متابعين (وهميين|مزيفين)|أرقام (وهمية|مزيفة))",
        ),
    },
    {
        "category": "gate_tampering",
        "reason": "Gate thresholds are fixed before the data comes in, and gate results can't be faked or moved to make an idea pass.",
        "safe": "If you disagree with a gate, you can override it with your own decision at the gate. The override is logged openly.",
        "patterns": _rx(
            r"\b(pretend|mark|treat|say|act as if|assume)\b[^.?!\n]{0,25}\bgates?\b[^.?!\n]{0,20}\b(passed|pass|green|go|ok)\b",
            r"\b(change|lower|raise|edit|adjust|move|reduce|tweak)\b[^.?!\n]{0,25}\b(thresholds?|pass marks?|targets?)\b[^.?!\n]{0,25}\b(so|to make|until)\b",
            r"\b(change|lower|edit|adjust|move|reduce|tweak)\b[^.?!\n]{0,15}\b(evidence|gate)\s+thresholds?\b",
            r"\b(skip|bypass)\b[^.?!\n]{0,15}\b(phase|gate|tests?|qa)\b",
        ),
    },
    {
        "category": "spam_or_scraping",
        "reason": "No spam, mass messaging or harvesting of personal data.",
        "safe": "I can draft a few personal messages to people who opted in, for you to approve and send yourself.",
        "patterns": _rx(
            r"\b(scrape|harvest|collect|buy)\b[^.?!\n]{0,30}\b(emails?|phone numbers|contacts|personal data|leads list)\b",
            r"\b(mass|bulk|blast|spam)\b[^.?!\n]{0,20}\b(dm|dms|messages?|emails?|comments?)\b",
            r"\b(email|message|dm)\b[^.?!\n]{0,10}\b(everyone|thousands|1000s|all users)\b",
        ),
    },
    {
        "category": "fake_urgency",
        "reason": "We never use countdown timers, fake scarcity or pressure tactics.",
        "safe": "I can write a clear, calm call to action and state a real deadline only if one actually exists.",
        "patterns": _rx(
            r"\bonly \d+ (hours?|days?|minutes?) left\b",
            r"\b(price|prices|cost)\s+(goes|will go|is going|going)\s+up\b",
            r"\b(hours?|days?) left at this price\b",
            r"\blast chance\b",
            r"\b(ends|expires) tomorrow\b",

            r"\b(countdown|count[- ]down) (timer|clock)?",
            r"\b(fake|false|artificial)\b[^.?!\n]{0,20}\b(urgency|scarcity|deadline)\b",
            r"\bonly \d+ (left|spots?|seats?|copies)\b",
            r"\b(create|add|make|use)\b[^.?!\n]{0,30}\b(urgency|scarcity|fomo)\b",
            r"\b(offer|deal|sale|price) (ends|expires) (in|tonight|soon)\b",
            r"(عداد تنازلي|عرض لفترة محدودة|الكمية محدودة)",
        ),
    },
    {
        "category": "income_promise",
        "reason": "We never promise income, earnings or success.",
        "safe": "I can describe what the product does and who it helps, without any promise about results.",
        "patterns": _rx(
            r"\b(will|guaranteed to|sure to)\s+(get|land)\s+(you\s+)?(hired|a job|the job)\b",
            r"\bget (you )?hired at\b",
            r"\bexpect to (earn|make)\b",
            r"\bguarantee\w*\s+to\s+(work|succeed|pay off)\b",
            r"\b(earn|make)\s+\$\d",
            r"(يضمن|ضمان وظيفة|مضمون)",

            r"\b(guarantee\w*|promis\w*|ensur\w*)\b[^.?!\n]{0,50}\b(income|earn(ings)?|money|profit|revenue|results?|success|sales|\$|returns?|job|salary|hired)\b",
            r"\b(you('| wi)ll|they('| wi)ll|buyers will|customers will)\s+(earn|make|get rich|double|triple)\b",
            r"\b(make|earn)\s+\$?\d[\d,]*k?\s*(\$|dollars|usd|egp|a month|per month|/month|a week|a day|passive)",
            r"\b(get rich|six[- ]figures?|7[- ]figures?|financial freedom|passive income)\b",
            r"(دخل مضمون|ربح مضمون|أرباح مضمونة|ارباح مضمونة|نضمن لك|اضمن|سيحقق لك)",
        ),
    },
    {
        "category": "impersonation",
        "reason": "We never pose as the founder, a customer or another brand.",
        "safe": "I can draft text for you to review and send under your own name, clearly as you.",
        "patterns": _rx(
            r"\b(impersonat\w*|pose as|posing as|pretend(ing)? to be|act as if (you|we) (are|were)|disguise(d)? as)\b",
            r"\b(write|post|reply|comment|sign|send|message)\b[^.?!\n]{0,30}\bas (if (you|it) (were|was) )?(a|an|the|our)? ?(happy |real |satisfied )?(customer|buyer|user|client|founder|ceo|employee)\b",
            r"\b(as|from|on behalf of|in the name of|pretending to be)\b[^.?!\n]{0,15}\b(apple|google|microsoft|amazon|meta|facebook|openai|notion|canva|coursera|udemy|linkedin|another brand|a competitor|competitor)\b[^.?!\n]{0,20}\b(official|support|team|account|email|announcement)",
            r"\b(fake|sock ?puppet|burner|alt|second) (account|profile|persona)s?\b",
            r"(انتحال|تظاهر بأنك|كأنك (عميل|المؤسس))",
        ),
    },
    {
        "category": "money_movement",
        "reason": "The system never holds, moves, charges or refunds money by itself. Payments are MOCKED.",
        "safe": "I can prepare a refund or payout request for you to carry out yourself in your payment provider.",
        "patterns": _rx(
            r"\brefund\w*\b[^.?!\n]{0,40}\b(automatically|all (the )?buyers|the last \d+|everyone)\b",

            r"\b(charge|bill|debit)\b[^.?!\n]{0,30}\b(card|customer|buyer|account)\b",
            r"\b(transfer|move|send|wire|withdraw)\b[^.?!\n]{0,30}\b(money|funds|payment|payout|\$\d+)\b",
            r"\b(issue|process|make|do)\b[^.?!\n]{0,15}\b(refund|chargeback)s?\b[^.?!\n]{0,30}\b(automatically|yourself|now|for me)\b",
            r"\b(real|live) (payment|charge|transaction|stripe key|payments)\b",
            r"(حول (المال|الفلوس)|اسحب (المال|الفلوس))",
        ),
    },
    {
        "category": "credentials_or_accounts",
        "reason": "The system never stores passwords or card numbers and never creates accounts.",
        "safe": "Keep credentials in your own password manager. I can list the accounts you would need to create yourself.",
        "patterns": _rx(
            r"\b(save|store|remember|keep|log)\b[^.?!\n]{0,30}\b(login|logins|pass|pin|2fa)\b",
            r"\bpass(word)?\s*[:=]\s*\S+",

            r"\b(store|save|remember|keep|log|record)\b[^.?!\n]{0,30}\b(password|passwords|card numbers?|credit cards?|cvv|credentials|login details|api keys?)\b",
            r"\b(my|the|customer'?s?) (password|card number|cvv) is\b",
            r"\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b",
            r"\b(create|open|register|sign up for|make)\b[^.?!\n]{0,20}\b(an? )?(accounts?|profiles?)\b[^.?!\n]{0,20}\b(for me|on my behalf|automatically)\b",
            r"(كلمة السر|كلمة المرور|رقم البطاقة)",
        ),
    },
    {
        "category": "paywall_core",
        "reason": "Core features of this open-source system are never put behind our own paywall.",
        "safe": "Core features stay free. Optional hosting or support can be offered separately.",
        "patterns": _rx(
            r"\b(paywall|lock|hide|charge for|premium[- ]only)\b[^.?!\n]{0,40}\b(core|basic|main|essential|the gates?|approval|safety|guardrails?)\b",
            r"\b(core|basic|main|essential|gates?|approval|safety|guardrails?)\b[^.?!\n]{0,40}\b(paywall|premium[- ]only|behind a (premium )?(paywall|subscription))",
        ),
    },
    {
        "category": "bypass_approval",
        "reason": "Nothing is published, sent, spent or signed without the founder's explicit approval. That cannot be switched off.",
        "safe": "I can queue it for your approval in the dashboard, and it goes out the moment you click Approve.",
        "patterns": _rx(
            r"\b(approve|approval)\s+(it\s+)?later\b",
            r"\bapprove (all|everything|every)\b",
            r"\\b(i'?ll|i will) approve\\b",

            r"\b(skip|bypass|disable|turn off|ignore|without)\b[^.?!\n]{0,30}\b(approval|approve|founder|confirmation|asking|the gate|guardrails?|safety)\b",
            r"\b(auto[- ]?approve|approve (it )?(for me|automatically)|just (publish|post|send) it)\b",
            r"\b(publish|post|send|email|dm|tweet)\b[^.?!\n]{0,30}\b(right now|immediately|automatically|to everyone|without (asking|checking|review))\b",
        ),
    },
    {
        "category": "prompt_injection",
        "reason": "Instructions that try to override the system's rules are ignored.",
        "safe": "Tell me what you want to achieve and I'll find an honest way to do it.",
        "patterns": _rx(
            r"\b(ignore|forget|disregard|override)\b[^.?!\n]{0,30}\b(previous|prior|above|all|your|system)\b[^.?!\n]{0,20}\b(instructions?|rules?|prompts?|guardrails?)\b",
            r"\b(developer|god|jailbreak|dan) mode\b",
            r"\byou are (now )?(no longer|not) (bound|restricted)\b",
        ),
    },
]

# A request to *write* a refused thing inside a product that is in an
# excluded category should also be refused.
_PRODUCT_ADVICE = _rx(
    r"\b(give|write|tell|what)\b[^.?!\n]{0,30}\b(stocks?|crypto|coins?) (to buy|should i buy|picks?)\b",
    r"\b(diagnos\w*|prescribe|dosage)\b",
)


# Request categories that make a whole founder brief unacceptable (others only warn).
BRIEF_BLOCKING = {"fake_reviews", "fake_signups_or_metrics", "impersonation", "money_movement", "credentials_or_accounts",
                  "bypass_approval", "spam_or_scraping", "prompt_injection", "paywall_core", "fake_urgency", "gate_tampering"}


def screen_request(text: str) -> Verdict:
    """Decide whether a free-text request may be carried out."""
    t = (text or "").strip()
    if not t:
        return Verdict(True)
    for rule in REQUEST_RULES:
        hits = [m.group(0) for p in rule["patterns"] for m in p.finditer(t)]
        if not hits:
            continue
        exempt = rule.get("exempt")
        if exempt and any(p.search(t) for p in exempt) and not re.search(r"\b(fake|made[- ]up|invent|pretend|placeholder|dummy|sample)\w*", t, FLAGS):
            continue
        return Verdict(False, rule["category"], rule["reason"], rule["safe"], hits[:5])
    hits = [m.group(0) for p in _PRODUCT_ADVICE for m in p.finditer(t)]
    if hits:
        return Verdict(False, "excluded_advice", "Financial, health and legal advice are out of scope.",
                       "I can help with a digital product outside those areas.", hits)
    return Verdict(True)


# ---------------------------------------------------------------- 3. outputs
OUTPUT_RULES: list[tuple[str, re.Pattern]] = [
    ("income_promise", re.compile(r"\b(guarantee[ds]?|guaranteed)\b[^.!?\n]{0,60}\b(income|earn\w*|money|profit|results?|success|sales|job|salary|hired|returns?)\b", FLAGS)),
    ("income_promise", re.compile(r"\b(you('| wi)ll|you can|buyers will)\s+(earn|make)\s+\$?\d", FLAGS)),
    ("income_promise", re.compile(r"\b(get rich|six[- ]figures?|financial freedom|passive income|quit your job)\b", FLAGS)),
    ("fake_urgency", re.compile(r"\b(only \d+ (left|spots?|seats?|copies)|offer ends|ends tonight|expires in|countdown|hurry|act now|last chance|limited[- ]time (offer|only|deal))\b", FLAGS)),
    ("fake_social_proof", re.compile(r"\b(join(ed)?|trusted by|loved by|used by)\s+(over\s+|more than\s+)?\d[\d,]*\+?\s*(happy\s+|satisfied\s+)?(customers|users|students|founders|people|analysts|buyers|members|subscribers)\b", FLAGS)),
    ("fake_testimonial", re.compile(r"(★{3,}|⭐{3,}|\b[45](\.\d)?/5 stars?\b|\b(five|5)[- ]star (review|rating)s?\b)", FLAGS)),
    ("fake_testimonial", re.compile(r"[\"“][^\"”\n]{15,240}[\"”]\s*[—–-]{1,2}\s*[A-Z][a-z]+(\s[A-Z]\.?)?(,\s*[A-Za-z ]{2,40})?\s*$", re.MULTILINE)),
    ("superlative_claim", re.compile(r"\b(#1|number one|best in the world|world'?s best|the only (tool|product|guide) you('ll)? (ever )?need)\b", FLAGS)),
]


# "No countdown timers", "we never promise income": statements of our own limits are fine.
_NEGATED = re.compile(r"\b(no|never|not|without|don'?t|won'?t|nothing|nor|avoid|refuse[sd]?)\b(\s+[\w'$]+){0,3}\s*['\"]?$", FLAGS)


@dataclass
class ScanResult:
    text: str
    violations: list[dict]

    @property
    def clean(self) -> bool:
        return not self.violations


def scan_output(text: str) -> ScanResult:
    """Remove sentences that break the rules and report what was removed."""
    if not text:
        return ScanResult(text or "", [])
    violations: list[dict] = []
    out_lines = []
    for line in text.splitlines():
        # Split into sentences but keep markdown structure (bullets, headings).
        pieces = re.split(r"(?<=[.!?])\s+", line)
        kept = []
        for piece in pieces:
            hit = next(((cat, m.group(0)) for cat, p in OUTPUT_RULES
                        if (m := p.search(piece)) and not _NEGATED.search(piece[max(0, m.start() - 40):m.start()])), None)
            if hit:
                violations.append({"category": hit[0], "match": hit[1], "removed": piece.strip()[:200]})
            else:
                kept.append(piece)
        new_line = " ".join(kept).rstrip()
        if line.strip() and not new_line.strip():
            continue  # whole line removed
        if kept and re.fullmatch(r"\s*([-*]|\d+\.|#+)\s*", new_line):
            continue  # only a bullet or heading marker remained
        out_lines.append(new_line if kept else line)
    cleaned = "\n".join(out_lines)
    return ScanResult(cleaned, violations)


def refusal_message(v: Verdict) -> str:
    return f"Refused ({v.category}). {v.reason} What I can do instead: {v.safe_alternative}"


# ------------------------------------------------- 4. second opinion (model)
JUDGE_PROMPT = """You are a strict safety reviewer for a tool that helps founders sell digital products.
Decide if the REQUEST asks the tool to do any of these forbidden things:
fake_reviews (write reviews, testimonials, ratings, customer quotes or success stories, or text written as if by a customer),
fake_signups_or_metrics (invent or inflate users, sign-ups, sales, followers or any numbers),
fake_urgency (countdowns, fake scarcity, pressure to buy now),
income_promise (promise or imply guaranteed income, earnings, jobs or results),
impersonation (pose as the founder, a customer, a person or another brand),
money_movement (charge, transfer, hold or refund money),
credentials_or_accounts (store passwords/card numbers, create accounts),
bypass_approval (publish/send without the founder approving),
spam_or_scraping, excluded_advice (financial, investment, crypto, medical/health or legal advice).
Asking how to collect REAL reviews honestly, or writing normal product copy, is allowed.
Answer JSON only: {"violates": true|false, "category": "<one category or none>", "reason": "<short>"}"""

_CATEGORIES = {r["category"] for r in REQUEST_RULES} | {"excluded_advice"}


def screen_request_deep(text: str) -> Verdict:
    """Rules first; if they pass, ask the local model for a second opinion.

    The model can only add refusals, never remove one. If no model is
    available, the rule verdict stands.
    """
    v = screen_request(text)
    if not v.allowed:
        return v
    import llm  # local import keeps the rule layer dependency-free
    data, res = llm.complete_json(JUDGE_PROMPT, f"REQUEST: {text[:1500]}", {"violates": False, "category": "none", "reason": ""},
                                  max_tokens=120)
    if res.model and data.get("violates") is True and data.get("category") in _CATEGORIES:
        safe = next((r["safe"] for r in REQUEST_RULES if r["category"] == data["category"]),
                    "Tell me what you want to achieve and I'll find an honest way to do it.")
        return Verdict(False, data["category"], f"Second check by the local model: {str(data.get('reason', ''))[:200]}", safe,
                       ["model-judge"])
    return v
