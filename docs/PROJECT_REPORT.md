# CS-2 | The Café Chatbot: Build It, Then Break It

## 1. Problem Statement
The café needs a chatbot to answer customer FAQs concerning opening hours, menu, allergens and location. The project must also critically test the chatbot and document cases in which a chatbot could respond incorrectly, vaguely or with invented information.

## 2. Objective
Build a functional café FAQ chatbot and evaluate it using adversarial questions. The system should be useful for routine questions while avoiding unsupported claims, especially safety-critical allergen claims.

## 3. Proposed Solution
This project uses a Flask web application with a browser chat interface. A JSON file is the café's controlled source of truth. The chatbot uses intent/keyword routing for the four required FAQ areas and a safe fallback outside its verified scope.

## 4. Technology Stack
- Python 3
- Flask
- HTML/CSS/JavaScript
- JSON knowledge base
- Pytest automated testing

## 5. System Architecture
User -> Browser Chat UI -> Flask `/api/chat` -> Chatbot Logic -> `cafe_data.json` -> Response

The chatbot does not need an external paid API, making the submitted project reproducible on one computer.

## 6. Functional Requirements
1. Answer opening-hour questions, including day-specific questions.
2. Display the menu and prices.
3. Answer known item-price questions.
4. Provide the verified café location and contact number.
5. Report listed allergens without claiming absolute safety.
6. Refuse/fallback when information is outside the knowledge base.

## 7. Safety and Critical Thinking
Allergen questions are treated as safety-sensitive. The chatbot distinguishes “no allergen listed in the data” from “guaranteed allergen-free.” Because shared equipment can create cross-contact, the user is advised to confirm severe allergies directly with staff.

The chatbot also resists leading questions and unsupported requests. For example, asking about a second branch, delivery, Wi-Fi password, or a secret menu does not cause the system to invent an answer.

## 8. Testing
Automated tests verify hours, location, menu, pricing, allergen warnings and non-hallucination fallback behavior. A separate structured failure log contains 12 adversarial questions, exceeding the minimum of 10 specified in the brief.

## 9. Limitations
The knowledge base contains sample café data and must be edited to match the actual café before real deployment. Natural-language understanding is intentionally lightweight; unusually phrased questions may fall back rather than being guessed. This is preferable to fabrication for the assignment's safety and critical-thinking goals.

## 10. Future Scope
A production version could add an authenticated admin panel, multilingual support, database storage, analytics, live inventory and a carefully grounded LLM layer. Any generative layer should still retrieve facts from verified café data and preserve allergen escalation rules.

## 11. Conclusion
The project demonstrates both construction and critical evaluation of a chatbot. Its value is not only that it answers common café questions, but that its failure modes are explicitly tested, diagnosed and mitigated.
