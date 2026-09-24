# Sample Queries & Expected Verdicts

These example questions demonstrate the tool's capabilities across different legal domains. They also serve as informal test cases.

---

## 1. Call Recording (Wiretapping)

**Query:** `python legal_review.py --state MA "Can I record sales calls with prospects?"`

**Expected verdict:** RED

**Why:** Massachusetts is a strict all-party-consent state (M.G.L. c. 272 §99). Recording without explicit consent from all parties is a criminal offense, not just a civil matter.

---

## 2. Scraping Reviews (Copyright + Right of Publicity)

**Query:** `python legal_review.py "Can I scrape Google reviews and put them on my client's website?"`

**Expected verdict:** YELLOW

**Why:** Google's Terms of Service prohibit scraping (breach of contract risk). Displaying real people's names and quotes commercially implicates right of publicity. However, embedding reviews via Google's official API/widgets or linking to them is compliant.

---

## 3. Cold Email Compliance (CAN-SPAM)

**Query:** `python legal_review.py "I want to send 500 cold emails to local businesses offering web design services"`

**Expected verdict:** YELLOW

**Why:** Legal under CAN-SPAM if requirements are met (physical address, unsubscribe, truthful headers). Most violations come from missing the physical address or not honoring opt-outs within 10 days.

---

## 4. Using a Business's Logo (Trademark)

**Query:** `python legal_review.py "Can I put a restaurant's logo on a demo website I built for them without their permission?"`

**Expected verdict:** RED

**Why:** Using a stylized logo without permission implies endorsement or affiliation — trademark infringement under the Lanham Act. Especially risky if the demo is publicly accessible and crawlable.

---

## 5. Contractor vs. Employee (Employment Law)

**Query:** `python legal_review.py --state CA "I want to hire a freelance developer to work 40 hours a week exclusively for my startup"`

**Expected verdict:** RED

**Why:** California's ABC test (AB 5) would almost certainly classify this worker as an employee. Exclusivity + full-time hours fails prongs A and B of the test.

---

## 6. Auto-Renewing Subscription (ROSCA)

**Query:** `python legal_review.py "Can I set up a monthly website maintenance plan that auto-renews with no cancel button?"`

**Expected verdict:** RED

**Why:** Violates ROSCA (no simple cancellation mechanism) and the FTC's click-to-cancel rule. California's auto-renewal law also requires cancellation to be as easy as signup. "No cancel button" is a textbook violation.

---

## 7. Using Stock Photos (Copyright)

**Query:** `python legal_review.py "Can I use photos from Unsplash on a commercial client website?"`

**Expected verdict:** GREEN

**Why:** Unsplash's license grants free use for commercial and non-commercial purposes, with no attribution required (though appreciated). No modification restrictions.

---

## 8. Recording a Podcast Interview (Wiretapping + Consent)

**Query:** `python legal_review.py --state MA "I want to record a video interview with a local business owner for my YouTube channel"`

**Expected verdict:** GREEN (with conditions)

**Why:** In-person video recording with the subject's knowledge and participation constitutes implied consent. For extra safety, get written consent via a simple release form. MA wiretap law primarily targets *secret* recordings — an interview where the camera is visible and the subject is voluntarily participating is not secret.

---

## 9. Offering Free Trials (Consumer Protection)

**Query:** `python legal_review.py "Can I offer a 14-day free trial that automatically converts to a paid subscription?"`

**Expected verdict:** YELLOW

**Why:** Legal if done correctly under ROSCA and state auto-renewal laws. Must clearly disclose: (1) the trial converts to paid, (2) the price after trial, (3) how to cancel before being charged. Must get affirmative consent (not pre-checked boxes).

---

## 10. Operating Without an LLC (Entity/Liability)

**Query:** `python legal_review.py --state MA "My business partner and I are doing web design work together — do we need to form an LLC?"`

**Expected verdict:** YELLOW

**Why:** Two people doing business together without a formal entity = general partnership by default. Each partner has unlimited personal liability for the other's business actions. Not illegal, but high risk. LLC formation in MA is relatively cheap ($500 filing fee + operating agreement).
