import os
import base64
import google.generativeai as genai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)

TOKEN = os.environ["TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

PROMPT = """Tu es un botaniste expert. Analyse cette photo de plante et donne les informations suivantes en français, de manière claire et structurée :

🌿 *Nom de la plante* : (nom commun et nom scientifique)
🏷️ *Famille botanique* : 
📝 *Description générale* : 
🌱 *Forme de vie* : (arbre, arbuste, herbe, liane...)
🌸 *Inflorescences* : 
🌺 *Fleurs* : (couleur, forme, taille...)
🍃 *Feuilles* : (forme, couleur, disposition...)

Si tu ne reconnais pas la plante, dis-le clairement."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌿 Bienvenue sur le Bot Botaniste !\n\n"
        "Envoie-moi une photo d'une plante et je t'identifie :\n"
        "• Le nom\n• La famille botanique\n• La description\n"
        "• La forme de vie\n• Les inflorescences\n• Les fleurs\n• Les feuilles"
    )

async def analyse_plante(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("🔍 Analyse en cours, patiente quelques secondes...")

        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        image_bytes = await file.download_as_bytearray()

        image_part = {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(image_bytes).decode("utf-8")
        }

        response = model.generate_content([PROMPT, image_part])
        resultat = response.text

        await update.message.reply_text(resultat, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"❌ Erreur : {e}")

app = ApplicationBuilder().token(TOKEN).connect_timeout(30).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, analyse_plante))

print("✅ Bot Botaniste lancé...")
app.run_polling()