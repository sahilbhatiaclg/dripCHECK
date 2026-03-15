# 🛠️ DripCheck Execution Plan (3-Hour Sprint)

### Phase 1: The Foundation (0:00 - 0:45)
- [ ] Initialize git and create `.env` with Gemini API Key.
- [ ] Setup Streamlit UI: Title, File Uploader, and Image Preview.
- [ ] Test Gemini Vision: Send 1 image + prompt "What is this?" to verify the connection.

- [ ] **Stitch Content uplaod PROMPT-** - "I used Stitch to design this 'Roast' interface. Can you write the Streamlit Python code (including custom CSS) to make my app look exactly like this screenshot?"

### Phase 2: The Core Logic (0:45 - 1:45)
- [ ] **Feature: The Identifier.** Prompt Gemini to return JSON (Color, Item, Style).
- [ ] **Step 2.1: The Pinterest Link Engine.** - **Ask Gemini for Keywords:** Update `app.py` prompts so Gemini returns short tags (e.g., "vintage oversized flannel").
    - **Clean the Keywords:** Use Python to replace spaces with `+` signs for URL compatibility.
    - **Build the Link:** Use `st.link_button` to create the interactive "See Inspo" element.
- [ ] **Feature: The Virtual Closet.** Use `st.session_state` to store multiple items.

### Phase 3: The "Vibe" Features (1:45 - 2:30)
- [ ] **Feature: Roast My Fit.** Button that triggers a snarky prompt.
- [ ] **Feature: Mood Setter.** Dropdown (Date, Exam, Party) that changes the styling logic.
- [ ] **Feature: Rate the Fit.** 1-10 score generator.

### Phase 4: Polish & Pitch (2:30 - 3:00)
- [ ] Add Custom CSS for "Dark Mode" or "Neon" vibes.
- [ ] Record a 30-second demo video (in case the Wi-Fi dies during judging!).