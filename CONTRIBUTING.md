# Contributing to PainToAd AI

Thank you for your interest in contributing to **PainToAd AI**! This project was initialized for the **AI for Marketers Hackathon**.

Please take a moment to review this document to ensure a smooth, collaborative workflow.

---

## 📜 Code of Conduct

We are committed to providing a welcoming, harassment-free experience for everyone. Please maintain professional communication and respect team members at all times.

---

## 🌿 Git Branching Strategy

We follow the Git Feature Branch workflow:

- `main`: Production-ready release branch. All code in `main` must pass tests and deployment builds.
- `develop`: Integration branch for active hackathon development.
- `feature/<feature-name>`: Individual feature branches (e.g., `feature/gemini-agent`, `feature/roi-analytics-dashboard`).
- `fix/<bug-name>`: Bug fix branches (e.g., `fix/cors-origin-issue`).

---

## 🛠️ Development Workflow

1. **Fork or Clone the Repository**:
   ```bash
   git clone https://github.com/HackIndiaXYZ/ai-for-marketers-hackathon-compass-crew.git
   cd ai-for-marketers-hackathon-compass-crew
   ```

2. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Follow Coding Standards**:
   - **Backend (Python)**: Follow PEP 8 guidelines. Type hint all function signatures. Use Pydantic schemas for data validation.
   - **Frontend (TypeScript / Next.js 15)**: Use strict TypeScript typing (`noImplicitAny`). Utilize Tailwind CSS and Shadcn UI primitives.
   - **Documentation**: Keep docstrings and markdown files updated.

4. **Commit Guidelines**:
   Use clear, descriptive commit messages:
   - `feat: add predictive CTR algorithm in backend analytics`
   - `fix: resolve CORS issue in FastAPI settings`
   - `docs: update deployment guidelines for Render`

5. **Submit a Pull Request (PR)**:
   - Push your branch to GitHub.
   - Open a Pull Request against the `develop` or `main` branch.
   - Fill out the PR template detailing changes made and verification steps.

---

## ✅ Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Code compiles without errors (`npm run build` for frontend, `pytest` for backend).
- [ ] No secret keys or credentials are committed to version control.
- [ ] New functionality is properly documented in `docs/` or `README.md`.
- [ ] All TODOs have been resolved.

---

## ❓ Need Assistance?

For questions regarding project architecture or backend utilities, reach out to the Team Lead (**Kamal Solanki**) or open an issue on the GitHub repository.
