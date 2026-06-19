# SCI19 3611 ARTIFICIAL INTELLIGENCE and SCI19 3631 Workshop AI

> **ฉบับปรับปรุงให้ทันสมัย พ.ศ. 2569 (Modernized Syllabus)** — อ้างอิงตำรา AIMA ฉบับที่ 4 (2020) และเพิ่มเนื้อหา Deep Learning, Transformers, LLMs, RAG, LLM Agents, Generative AI และ AI Ethics & Safety.
> รายละเอียดฉบับเต็มอยู่ใน [`TQF3_AI_Modernized.docx`](./TQF3_AI_Modernized.docx) (มคอ.3). เวอร์ชันเดิมเก็บไว้ที่ [`README_OLD_AIMA3.md`](./README_OLD_AIMA3.md).

**Instructor:** Asst. Prof. Dr. Ittipon Fongkaew  
**Email:** ittipon@g.sut.ac.th

**Classroom:** B6103-A (13:00–16:00)  
**Lab Workshop:** DIGITAL TECH LAB 03 (13:00–15:00)

**Resources:**  
[GitHub Repository](https://github.com/aofphy/SCI193611_ARTIFICIAL_INTELLIGENCE.git)

---

## 📘 Course Overview

This course introduces fundamental concepts and techniques in Artificial Intelligence, combining theoretical foundations with practical applications in Python. Content spans **Classical AI** — Search, Logic & Planning, and Probabilistic Reasoning — through to **Modern AI** — Deep Learning, the Transformer architecture, Large Language Models (LLMs), RAG, LLM Agents, and Generative AI — along with **AI Ethics & Safety**.

The course is designed to complement the parallel Machine Learning course, deliberately avoiding overlapping Classical ML content (regression, classification, decision trees) and reinvesting that time into Classical AI (Logic & Planning) and the modern LLM/Agent/Generative AI track.

**Textbook:**  
Stuart Russell, Peter Norvig – *Artificial Intelligence: A Modern Approach* (**4th Edition, 2020**)

---

## 🎯 Learning Outcomes

By the end of this course, you will be able to:

1. Understand **Agent-Based AI** and design **Rational Agents**.
2. Apply **Search & Adversarial Search** techniques, including **MCTS**.
3. Use **Logic & Automated Planning** for knowledge representation and problem solving.
4. Analyze **Probabilistic & Bayesian models**.
5. Build and train **Neural Networks & Deep Learning** models with **PyTorch**.
6. Explain the **Transformer architecture** and how **Large Language Models** work.
7. Develop **RAG** applications and **LLM Agents** using tools / function calling.
8. Apply **Generative AI** (Diffusion, Multimodal) and understand **RLHF**.
9. Evaluate AI capabilities, limitations, and **ethics/safety** issues, including **AGI**.

---

## 🗓️ Schedule & Topics (15 Weeks)

| Week | Main Topics | Activities / Lab / Assessment |
| --- | --- | --- |
| 1 | Introduction to AI – history, evolution, and the modern Generative AI landscape | Orientation, tooling setup (Python / Google Colab) |
| 2 | Intelligent Agents – architecture, Rational Agents, LLM-based Agents | Tutorial: Agent design |
| 3 | Problem Solving by Search – BFS, DFS, UCS, A* | Project 0: Search Algorithms |
| 4 | Adversarial Search – Minimax, Alpha-Beta Pruning, MCTS | Exercise 1 (HexaPawn) |
| 5 | Logic & Automated Planning – Propositional/First-Order Logic, Knowledge Representation | Project 1: Search & Planning |
| 6 | Quantifying Uncertainty & Probabilistic Reasoning – Bayes Rule, Bayesian Networks | Exercise 2 |
| 7 | Reasoning Over Time – Markov Models, HMMs | Exercise 3 |
| — | **Midterm Examination** (covers Weeks 1–7) | — |
| 8 | Neural Networks – Perceptron, Backpropagation, training (PyTorch) | Lab: PyTorch basics |
| 9 | Deep Learning – CNNs, Computer Vision, Transfer Learning | Lab: Image Classifier |
| 10 | Sequence Models & The Transformer Architecture – Attention | Exercise 4 |
| 11 | Large Language Models – Pre-training, Fine-tuning, Prompting | Lab: Fine-tune & Prompt |
| 12 | Retrieval-Augmented Generation (RAG) & LLM Agents – Tool Use, Function Calling | Lab: Build an LLM Agent |
| 13 | Generative AI – Diffusion, Multimodal, Image/Audio Generation + RLHF | Exercise 5 |
| 14 | AI Ethics, Safety & Alignment – Bias, Governance, AGI | Discussion / Debate |
| 15 | Project Presentations & the Future of AI | Final Project Presentation |
| — | **Final Examination** (covers Weeks 8–15) | — |

---

## 💻 Projects & Assignments

- **Project 0 — Search Algorithms:** implement BFS, DFS, UCS, and A* on maze/game problems.
- **Project 1 — Search & Planning:** solve problems with automated planning and logical knowledge representation.
- **Lab — LLM Agent:** build an agent using RAG and tool/function calling with Hugging Face / an LLM API.
- **Final Project:** build a real AI application (RAG Chatbot, LLM Agent, Image Classifier, or Generative AI app) and present it.
- **Weekly Exercises:** aligned with each week's topic.

**Grading:**

| Assessment Component | Weight |
| --- | --- |
| Homework & Exercises | 20% |
| Projects (Search, Planning, LLM Agent Lab) | 30% |
| Midterm Examination | 20% |
| Final Project + Presentation | 20% |
| Attendance & Participation | 10% |
| **Total** | **100%** |

**Grading Scale:** A: 80–100 · B+: 75–79 · B: 70–74 · C+: 65–69 · C: 60–64 · D+: 55–59 · D: 50–54 · F: 0–49  
*(เกณฑ์อาจปรับตามดุลยพินิจของอาจารย์และระเบียบของสถาบัน)*

---

## 📂 Course Materials Map 

ตารางจับคู่กิจกรรม (Tutorial / Project / Exercise / Lab) กับเนื้อหารายสัปดาห์และไฟล์จริงในรีโพ. ช่อง "—" หมายถึงสื่อที่ยังต้องจัดทำเพิ่มสำหรับเนื้อหาสมัยใหม่.

| Week | Topic | Activity | Material in repo |
| --- | --- | --- | --- |
| 1 | Introduction to AI | **Tutorial:** Python / Colab setup | [`python-tutorial/`](./python-tutorial) · [`slide/lec0.pdf`](./slide/lec0.pdf), [`slide/lecture1.pdf`](./slide/lecture1.pdf) |
| 2 | Intelligent Agents | **Tutorial:** Agent design | [`python-tutorial/tutorial_code/exercises/`](./python-tutorial/tutorial_code/exercises) · [`slide/lecture2.pdf`](./slide/lecture2.pdf) |
| 3 | Search – BFS/DFS/UCS/A* | **Project 0:** Search Algorithms | [`projects/project0/`](./projects/project0) · [`slide/lecture3_th.pdf`](./slide/lecture3_th.pdf) |
| 4 | Adversarial Search – Minimax, MCTS | **Exercise 1 (HexaPawn)** + Minimax agent | [`slide/hexapawact.pdf`](./slide/hexapawact.pdf), [`hexapaw.html`](./hexapaw.html), [`gameHexaPawn.html`](./gameHexaPawn.html), [`projects/project1/`](./projects/project1) (Minimax) · [`slide/lecture4_th.pdf`](./slide/lecture4_th.pdf) |
| 5 | Logic & Automated Planning | **Project 1:** Search & Planning | [`labs/w05_logic_planning.ipynb`](./labs/w05_logic_planning.ipynb) *(runnable)* |
| 6 | Probabilistic Reasoning – Bayes Nets | **Exercise 2** | [`code/lecture5-cherries.ipynb`](./code/lecture5-cherries.ipynb) · [`slide/lecture5_th.pdf`](./slide/lecture5_th.pdf) |
| 7 | Reasoning Over Time – Markov, HMM | **Exercise 3** + Bayes Filter | [`exercises/e3_nosol.pdf`](./exercises/e3_nosol.pdf), [`code/lecture6-forward-backward.ipynb`](./code/lecture6-forward-backward.ipynb), [`code/particle-filtering/`](./code/particle-filtering), [`code/exercises-4-kalman.ipynb`](./code/exercises-4-kalman.ipynb), [`projects/project2/`](./projects/project2) (Bayes Filter) · [`slide/lecture6_th.pdf`](./slide/lecture6_th.pdf) |
| 8 | Neural Networks (PyTorch) | **Lab:** PyTorch basics | [`code/lecture7-spiral.ipynb`](./code/lecture7-spiral.ipynb) · [`slide/lecture7_thai.pdf`](./slide/lecture7_thai.pdf) |
| 9 | Deep Learning – CNNs | **Lab:** Image Classifier | [`code/lecture7-convnet.ipynb`](./code/lecture7-convnet.ipynb) · [`slide/lecture8_thai.pdf`](./slide/lecture8_thai.pdf) |
| 10 | Transformer Architecture | **Exercise 4** | [`labs/w10_transformer.ipynb`](./labs/w10_transformer.ipynb) *(runnable)* |
| 11 | Large Language Models | **Lab:** Fine-tune & Prompt | [`labs/w11_llm_finetune_prompt.ipynb`](./labs/w11_llm_finetune_prompt.ipynb) *(Colab GPU)* |
| 12 | RAG & LLM Agents | **Lab:** Build an LLM Agent | [`labs/w12_rag_agent.ipynb`](./labs/w12_rag_agent.ipynb) *(runnable)* |
| 13 | Generative AI + RLHF | **Exercise 5** | [`labs/w13_generative_ai.ipynb`](./labs/w13_generative_ai.ipynb) *(Colab GPU)* |
| 14 | AI Ethics, Safety & Alignment | **Discussion / Debate** | — *(ต้องจัดทำใหม่: หัวข้ออภิปราย)* |
| 15 | Project Presentations | **Final Project** | [`projects/`](./projects) (ต่อยอดเป็น final project) |

**สื่อเสริม / legacy (นอกแกนหลัก 15 สัปดาห์):** [`code/lecture8-mdp.ipynb`](./code/lecture8-mdp.ipynb) และ [`code/q-learning-demo/`](./code/q-learning-demo) (MDP & Reinforcement Learning) — ใช้ประกอบหัวข้อ Decision/RLHF ได้ตามความเหมาะสม.

---

## 🛠️ Prerequisites & Setup

**Prerequisites:**
- Python programming (basic NumPy, pandas, matplotlib)
- Basic math: Linear Algebra, Calculus, and Probability

**Tools & Software:**
- **Anaconda Platform** – [Download](https://www.anaconda.com/)
- **Visual Studio Code** – [Download](https://code.visualstudio.com/)
- **Google Colab** (for GPU work: Deep Learning and LLMs)
- Core libraries: **PyTorch**, **Hugging Face Transformers**, TensorFlow/Keras
- LLM tooling: **LangChain** or **LlamaIndex**, Vector DB (FAISS / Chroma) for RAG
- Support libraries: NumPy, pandas, matplotlib, seaborn

### Recommended Resources

- Russell & Norvig — *Artificial Intelligence: A Modern Approach* (4th Ed., 2020) — *primary textbook*
- Goodfellow, Bengio & Courville — *Deep Learning* (MIT Press)
- Hugging Face — NLP/LLM Course and Transformers documentation (online)
- Jurafsky & Martin — *Speech and Language Processing* (3rd Ed. draft, online)
- Official docs for [PyTorch](https://pytorch.org/), [Hugging Face Transformers](https://huggingface.co/docs/transformers), and LangChain/LlamaIndex
- [Python Data Science Handbook](https://github.com/jakevdp/PythonDataScienceHandbook), [scikit-learn](https://scikit-learn.org/stable/)

---

## 📚 License & Acknowledgements

This course material is for educational purposes. The core textbook content belongs to the respective authors and publishers.

---

> **Note:** For detailed instructions and the latest updates, refer to the [GitHub Repository](https://github.com/aofphy/SCI193611_ARTIFICIAL_INTELLIGENCE.git).

> **tool:**
> - HexaPawn random Tools — [link](https://script.google.com/macros/s/AKfycbwZbR1ANc-vn_shok9lHtHCWOogzCt8fbsJabfxN0IAkB5QhFY1-8nPxMPzaNa7donrrg/exec)
> - HexaPawn gameplay — [link](https://script.google.com/macros/s/AKfycbzA75-egsQ1B7hNQA7vaXnQy_IvOtgeVkrtk9KCqRFYk3NU7PXdwcsbR2hVyk1proBwfw/exec)
