def load_css():
    return """
<style>

/* ===============================
   GLOBAL
================================ */

html, body, [class*="css"]{
    background:#0d1117;
    color:white;
    font-family:Inter,sans-serif;
}

/* ===============================
   APP
================================ */

.main{
    background:#0d1117;
    padding-top:2rem;
}

/* ===============================
   TITLE
================================ */

.main-title{
    font-size:42px;
    font-weight:800;
    text-align:center;
    margin-bottom:10px;

    background:linear-gradient(
        90deg,
        #58a6ff,
        #7ee787,
        #d2a8ff
    );

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.subtitle{

    text-align:center;

    color:#8b949e;

    font-size:18px;

    margin-bottom:35px;

}

/* ===============================
   REPOSITORY CARD
================================ */

.repo-card{

    background:#161b22;

    border-radius:16px;

    padding:20px;

    border:1px solid #30363d;

    margin-bottom:25px;

    box-shadow:

        0px 6px 25px rgba(0,0,0,.35);

}

/* ===============================
   CHAT BOX
================================ */

.chat-container{

    background:#161b22;

    border-radius:18px;

    padding:20px;

    border:1px solid #30363d;

    box-shadow:

        0px 8px 30px rgba(0,0,0,.35);

}

/* ===============================
   USER MESSAGE
================================ */

.user-message{

    background:#238636;

    padding:14px 18px;

    border-radius:18px 18px 4px 18px;

    margin:10px 0;

    color:white;

    width:fit-content;

    margin-left:auto;

    max-width:80%;

    font-size:15px;

}

/* ===============================
   ASSISTANT MESSAGE
================================ */

.bot-message{

    background:#21262d;

    padding:14px 18px;

    border-radius:18px 18px 18px 4px;

    margin:10px 0;

    color:white;

    width:fit-content;

    max-width:80%;

    border:1px solid #30363d;

    font-size:15px;

}

/* ===============================
   BUTTON
================================ */

.stButton>button{

    width:100%;

    height:48px;

    border:none;

    border-radius:12px;

    font-size:16px;

    font-weight:700;

    color:white;

    background:

        linear-gradient(
            90deg,
            #238636,
            #2ea043
        );

    transition:0.3s;

}

.stButton>button:hover{

    transform:translateY(-2px);

    box-shadow:

        0px 10px 20px rgba(46,160,67,.4);

}

/* ===============================
   TEXT INPUTS
================================ */

.stTextInput input{

    background:#0d1117;

    color:white;

    border:1px solid #30363d;

    border-radius:10px;

}

/* ===============================
   TEXT AREA
================================ */

.stTextArea textarea{

    background:#0d1117;

    color:white;

    border:1px solid #30363d;

    border-radius:10px;

}

/* ===============================
   SIDEBAR
================================ */

[data-testid="stSidebar"]{

    background:#161b22;

    border-right:1px solid #30363d;

}

/* ===============================
   SCROLLBAR
================================ */

::-webkit-scrollbar{

    width:8px;

}

::-webkit-scrollbar-thumb{

    background:#30363d;

    border-radius:10px;

}

::-webkit-scrollbar-thumb:hover{

    background:#58a6ff;

}

</style>
"""