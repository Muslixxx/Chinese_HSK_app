"""Streamlit UI for an HSK1 vocabulary quiz.

Run with: `streamlit run Main.py`
"""

import random
from typing import Dict, List, Optional

import streamlit as st


def _trigger_rerun() -> None:
    """Force a rerun compatible with both legacy and modern Streamlit."""
    rerun = getattr(st, "rerun", None)
    if callable(rerun):
        rerun()
        return
    experimental_rerun = getattr(st, "experimental_rerun", None)
    if callable(experimental_rerun):
        experimental_rerun()
        return
    raise RuntimeError("Streamlit rerun API unavailable in this version.")


HSK1_VOCAB: List[Dict[str, str]] = [
    {"hanzi": "爱", "pinyin": "ài", "translation": "aimer"},
    {"hanzi": "八", "pinyin": "bā", "translation": "huit"},
    {"hanzi": "爸爸", "pinyin": "bàba", "translation": "papa"},
    {"hanzi": "杯子", "pinyin": "bēizi", "translation": "tasse; verre"},
    {"hanzi": "北京", "pinyin": "Běijīng", "translation": "Pékin"},
    {"hanzi": "本", "pinyin": "běn", "translation": "classificateur (livres)"},
    {"hanzi": "不", "pinyin": "bù", "translation": "ne pas"},
    {"hanzi": "不客气", "pinyin": "bú kèqi", "translation": "de rien"},
    {"hanzi": "菜", "pinyin": "cài", "translation": "plat; légumes"},
    {"hanzi": "茶", "pinyin": "chá", "translation": "thé"},
    {"hanzi": "吃", "pinyin": "chī", "translation": "manger"},
    {"hanzi": "出租车", "pinyin": "chūzūchē", "translation": "taxi"},
    {"hanzi": "大学", "pinyin": "dàxué", "translation": "université"},
    {"hanzi": "大", "pinyin": "dà", "translation": "grand"},
    {"hanzi": "的", "pinyin": "de", "translation": "particule possessive"},
    {"hanzi": "点", "pinyin": "diǎn", "translation": "heure; point"},
    {"hanzi": "电脑", "pinyin": "diànnǎo", "translation": "ordinateur"},
    {"hanzi": "电视", "pinyin": "diànshì", "translation": "télévision"},
    {"hanzi": "电影", "pinyin": "diànyǐng", "translation": "film"},
    {"hanzi": "东西", "pinyin": "dōngxi", "translation": "chose; objet"},
    {"hanzi": "都", "pinyin": "dōu", "translation": "tous"},
    {"hanzi": "对不起", "pinyin": "duìbuqǐ", "translation": "désolé"},
    {"hanzi": "多", "pinyin": "duō", "translation": "beaucoup"},
    {"hanzi": "多少", "pinyin": "duōshao", "translation": "combien"},
    {"hanzi": "儿子", "pinyin": "érzi", "translation": "fils"},
    {"hanzi": "饭馆", "pinyin": "fànguǎn", "translation": "restaurant"},
    {"hanzi": "飞机", "pinyin": "fēijī", "translation": "avion"},
    {"hanzi": "分钟", "pinyin": "fēnzhōng", "translation": "minute"},
    {"hanzi": "高兴", "pinyin": "gāoxìng", "translation": "content"},
    {"hanzi": "个", "pinyin": "gè", "translation": "classificateur général"},
    {"hanzi": "工作", "pinyin": "gōngzuò", "translation": "travail; travailler"},
    {"hanzi": "汉语", "pinyin": "Hànyǔ", "translation": "langue chinoise"},
    {"hanzi": "好", "pinyin": "hǎo", "translation": "bien; bon"},
    {"hanzi": "喝", "pinyin": "hē", "translation": "boire"},
    {"hanzi": "很", "pinyin": "hěn", "translation": "très"},
    {"hanzi": "回", "pinyin": "huí", "translation": "revenir"},
    {"hanzi": "会", "pinyin": "huì", "translation": "savoir faire; réunion"},
    {"hanzi": "家", "pinyin": "jiā", "translation": "famille; maison"},
    {"hanzi": "叫", "pinyin": "jiào", "translation": "s'appeler; appeler"},
    {"hanzi": "今天", "pinyin": "jīntiān", "translation": "aujourd'hui"},
    {"hanzi": "看", "pinyin": "kàn", "translation": "regarder; lire"},
    {"hanzi": "来", "pinyin": "lái", "translation": "venir"},
    {"hanzi": "老师", "pinyin": "lǎoshī", "translation": "professeur"},
    {"hanzi": "冷", "pinyin": "lěng", "translation": "froid"},
    {"hanzi": "里", "pinyin": "lǐ", "translation": "dans; intérieur"},
    {"hanzi": "妈妈", "pinyin": "māma", "translation": "maman"},
    {"hanzi": "吗", "pinyin": "ma", "translation": "particule interrogative"},
    {"hanzi": "买", "pinyin": "mǎi", "translation": "acheter"},
    {"hanzi": "猫", "pinyin": "māo", "translation": "chat"},
    {"hanzi": "没关系", "pinyin": "méi guānxi", "translation": "ce n'est rien"},
    {"hanzi": "米饭", "pinyin": "mǐfàn", "translation": "riz cuit"},
    {"hanzi": "明天", "pinyin": "míngtiān", "translation": "demain"},
    {"hanzi": "名字", "pinyin": "míngzi", "translation": "nom; prénom"},
    {"hanzi": "哪儿", "pinyin": "nǎr", "translation": "où"},
    {"hanzi": "那", "pinyin": "nà", "translation": "cela"},
    {"hanzi": "你", "pinyin": "nǐ", "translation": "tu; vous"},
    {"hanzi": "朋友", "pinyin": "péngyou", "translation": "ami"},
    {"hanzi": "漂亮", "pinyin": "piàoliang", "translation": "joli"},
    {"hanzi": "苹果", "pinyin": "píngguǒ", "translation": "pomme"},
    {"hanzi": "请", "pinyin": "qǐng", "translation": "s'il vous plaît; inviter"},
    {"hanzi": "去", "pinyin": "qù", "translation": "aller"},
    {"hanzi": "热", "pinyin": "rè", "translation": "chaud"},
    {"hanzi": "认识", "pinyin": "rènshi", "translation": "connaître"},
    {"hanzi": "三", "pinyin": "sān", "translation": "trois"},
    {"hanzi": "商店", "pinyin": "shāngdiàn", "translation": "magasin"},
    {"hanzi": "上班", "pinyin": "shàngbān", "translation": "aller au travail"},
    {"hanzi": "上午", "pinyin": "shàngwǔ", "translation": "matinée"},
    {"hanzi": "少", "pinyin": "shǎo", "translation": "peu"},
    {"hanzi": "什么", "pinyin": "shénme", "translation": "quoi"},
    {"hanzi": "是", "pinyin": "shì", "translation": "être"},
    {"hanzi": "书", "pinyin": "shū", "translation": "livre"},
    {"hanzi": "水", "pinyin": "shuǐ", "translation": "eau"},
    {"hanzi": "睡觉", "pinyin": "shuìjiào", "translation": "dormir"},
    {"hanzi": "说", "pinyin": "shuō", "translation": "parler; dire"},
    {"hanzi": "四", "pinyin": "sì", "translation": "quatre"},
    {"hanzi": "他", "pinyin": "tā", "translation": "il; lui"},
    {"hanzi": "她", "pinyin": "tā", "translation": "elle"},
    {"hanzi": "太", "pinyin": "tài", "translation": "trop"},
    {"hanzi": "天气", "pinyin": "tiānqì", "translation": "météo"},
    {"hanzi": "听", "pinyin": "tīng", "translation": "écouter"},
    {"hanzi": "同学", "pinyin": "tóngxué", "translation": "camarade de classe"},
    {"hanzi": "喂", "pinyin": "wèi", "translation": "allô"},
    {"hanzi": "我", "pinyin": "wǒ", "translation": "je; moi"},
    {"hanzi": "我们", "pinyin": "wǒmen", "translation": "nous"},
    {"hanzi": "五", "pinyin": "wǔ", "translation": "cinq"},
    {"hanzi": "喜欢", "pinyin": "xǐhuan", "translation": "aimer bien"},
    {"hanzi": "下", "pinyin": "xià", "translation": "descendre; prochain"},
    {"hanzi": "下午", "pinyin": "xiàwǔ", "translation": "après-midi"},
    {"hanzi": "下雨", "pinyin": "xiàyǔ", "translation": "pleuvoir"},
    {"hanzi": "先生", "pinyin": "xiānsheng", "translation": "monsieur"},
    {"hanzi": "现在", "pinyin": "xiànzài", "translation": "maintenant"},
    {"hanzi": "想", "pinyin": "xiǎng", "translation": "vouloir; penser"},
    {"hanzi": "小", "pinyin": "xiǎo", "translation": "petit"},
    {"hanzi": "小姐", "pinyin": "xiǎojiě", "translation": "mademoiselle"},
    {"hanzi": "写", "pinyin": "xiě", "translation": "écrire"},
    {"hanzi": "谢谢", "pinyin": "xièxie", "translation": "merci"},
    {"hanzi": "星期", "pinyin": "xīngqī", "translation": "semaine"},
    {"hanzi": "学生", "pinyin": "xuésheng", "translation": "étudiant"},
    {"hanzi": "学习", "pinyin": "xuéxí", "translation": "étudier"},
    {"hanzi": "学校", "pinyin": "xuéxiào", "translation": "école"},
    {"hanzi": "一", "pinyin": "yī", "translation": "un"},
    {"hanzi": "一点儿", "pinyin": "yìdiǎnr", "translation": "un peu"},
    {"hanzi": "医生", "pinyin": "yīshēng", "translation": "médecin"},
    {"hanzi": "医院", "pinyin": "yīyuàn", "translation": "hôpital"},
    {"hanzi": "椅子", "pinyin": "yǐzi", "translation": "chaise"},
    {"hanzi": "有", "pinyin": "yǒu", "translation": "avoir"},
    {"hanzi": "月", "pinyin": "yuè", "translation": "mois; lune"},
    {"hanzi": "在", "pinyin": "zài", "translation": "être à; en train de"},
    {"hanzi": "再见", "pinyin": "zàijiàn", "translation": "au revoir"},
    {"hanzi": "怎么", "pinyin": "zěnme", "translation": "comment"},
    {"hanzi": "怎么样", "pinyin": "zěnmeyàng", "translation": "comment est-ce"},
    {"hanzi": "这", "pinyin": "zhè", "translation": "ceci"},
    {"hanzi": "中国", "pinyin": "Zhōngguó", "translation": "Chine"},
    {"hanzi": "中午", "pinyin": "zhōngwǔ", "translation": "midi"},
    {"hanzi": "住", "pinyin": "zhù", "translation": "habiter"},
    {"hanzi": "桌子", "pinyin": "zhuōzi", "translation": "table"},
    {"hanzi": "字", "pinyin": "zì", "translation": "caractère; mot"},
    {"hanzi": "昨天", "pinyin": "zuótiān", "translation": "hier"},
    {"hanzi": "左边", "pinyin": "zuǒbian", "translation": "gauche"},
]


def build_question_pool(
    vocab: List[Dict[str, str]], num_questions: int, num_choices: int = 4, seed: Optional[int] = None
) -> List[Dict[str, str]]:
    """Build a randomized quiz question list."""
    rng = random.Random(seed)
    total_questions = min(num_questions, len(vocab))
    selected = rng.sample(vocab, k=total_questions)

    translations = [entry["translation"] for entry in vocab]
    questions = []
    for entry in selected:
        incorrect_pool = [t for t in translations if t != entry["translation"]]
        incorrect_choices = rng.sample(incorrect_pool, k=min(num_choices - 1, len(incorrect_pool)))
        choices = incorrect_choices + [entry["translation"]]
        rng.shuffle(choices)
        questions.append(
            {
                "hanzi": entry["hanzi"],
                "pinyin": entry["pinyin"],
                "correct": entry["translation"],
                "choices": choices,
            }
        )
    return questions


def reset_quiz(num_questions: int, seed: Optional[int] = None) -> None:
    """Initialize session state for a new quiz."""
    st.session_state["num_questions"] = num_questions
    st.session_state["questions"] = build_question_pool(HSK1_VOCAB, num_questions, seed=seed)
    st.session_state["current_idx"] = 0
    st.session_state["score"] = 0
    st.session_state["answered"] = False
    st.session_state["last_choice"] = None
    st.session_state["feedback"] = ""
    st.session_state["history"] = []


def evaluate_answer(choice: str) -> None:
    """Evaluate the selected answer and update session state."""
    idx = st.session_state["current_idx"]
    question = st.session_state["questions"][idx]
    is_correct = choice == question["correct"]

    st.session_state["answered"] = True
    st.session_state["last_choice"] = choice
    if is_correct:
        st.session_state["score"] += 1
        st.session_state["feedback"] = "✅ Bonne réponse !"
    else:
        st.session_state["feedback"] = (
            f"❌ Mauvaise réponse. La bonne traduction est **{question['correct']}**."
        )

    st.session_state["history"].append(
        {
            "hanzi": question["hanzi"],
            "pinyin": question["pinyin"],
            "correct": question["correct"],
            "user_choice": choice,
            "is_correct": is_correct,
        }
    )


def render_summary() -> None:
    """Display final quiz summary."""
    score = st.session_state["score"]
    total = len(st.session_state["questions"])
    st.success(f"Quiz terminé ! Vous avez {score} bonne(s) réponse(s) sur {total}.")

    details = []
    for entry in st.session_state["history"]:
        status = "✅" if entry["is_correct"] else "❌"
        details.append(
            {
                "Mot": entry["hanzi"],
                "Pinyin": entry["pinyin"],
                "Votre réponse": entry["user_choice"],
                "Bonne réponse": entry["correct"],
                "Résultat": status,
            }
        )
    if details:
        st.subheader("Vos réponses")
        st.table(details)


def render_quiz() -> None:
    """Render the quiz interface."""
    idx = st.session_state["current_idx"]
    questions = st.session_state["questions"]
    question = questions[idx]
    total = len(questions)

    st.write(f"Question {idx + 1} sur {total}")
    st.progress((idx + 1) / total)

    st.markdown(f"### {question['hanzi']}")
    st.caption(f"Pinyin : {question['pinyin']}")

    if not st.session_state["answered"]:
        with st.form(key=f"quiz_form_{idx}"):
            choice = st.selectbox(
                "Choisissez la traduction correcte :",
                question["choices"],
                index=None,
                placeholder="Sélectionnez une réponse",
                key=f"choice_select_{idx}",
            )
            submitted = st.form_submit_button("Valider la réponse")

        if submitted:
            if choice is None:
                st.warning("Sélectionnez une réponse avant de valider.")
            else:
                evaluate_answer(choice)
                _trigger_rerun()
    else:
        st.info(st.session_state["feedback"])
        correct_answer = question["correct"]
        st.write(f"Traduction correcte : **{correct_answer}**")

        if st.button("Question suivante", key=f"next_button_{idx}"):
            st.session_state["current_idx"] += 1
            st.session_state["answered"] = False
            st.session_state["last_choice"] = None
            st.session_state["feedback"] = ""
            _trigger_rerun()


def main() -> None:
    st.set_page_config(page_title="Quiz vocabulaire HSK1", page_icon="📘", layout="centered")
    st.title("Quiz vocabulaire HSK1")
    st.write(
        "Testez vos connaissances en vocabulaire du HSK 1. "
        "Choisissez la bonne traduction pour chaque caractère."
    )

    st.sidebar.header("Paramètres")
    default_num = st.session_state.get("num_questions", 10)
    max_questions = len(HSK1_VOCAB)
    num_questions = st.sidebar.slider(
        "Nombre de questions",
        min_value=5,
        max_value=max_questions,
        value=min(default_num, max_questions),
    )

    if st.sidebar.button("Lancer un nouveau quiz"):
        seed = random.randint(0, 10_000)
        reset_quiz(num_questions, seed=seed)
        _trigger_rerun()

    if "questions" not in st.session_state:
        reset_quiz(num_questions)

    st.sidebar.metric("Score", f"{st.session_state['score']} / {len(st.session_state['questions'])}")

    if st.session_state["current_idx"] >= len(st.session_state["questions"]):
        render_summary()
    else:
        render_quiz()


if __name__ == "__main__":
    main()
