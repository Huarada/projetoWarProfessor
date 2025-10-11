// src/components/GeneralChat.jsx
import { useState } from "react"
import { analyzeMove } from "@/services/gameApi"
import ReactMarkdown from "react-markdown"
import generalImg from '../assets/general.png'


export default function GeneralChat({ gameId }) {
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState([
    { from: "general", text: "👋 Olá, comandante! Pronto para analisar sua jogada?" }
  ])
  const [input, setInput] = useState("")

  // 🔹 Envio de mensagens livres ao backend
  async function sendMessage(text) {
    if (!text.trim()) return
    const userMessage = { from: "user", text }
    setMessages(m => [...m, userMessage])
    setInput("")

    try {
      const res = await fetch(`/api/general/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ game_id: gameId, message: text }),
      })
      const data = await res.json()
      const reply = { from: "general", text: data.reply || data.message || "⚠️ Sem resposta." }
      setMessages(m => [...m, reply])
    } catch (e) {
      setMessages(m => [...m, { from: "general", text: "❌ Erro ao responder." }])
    }
  }

  // 🔹 Botão extra: análise de jogada
  async function handleAnalyze() {
    if (!gameId) {
      setMessages(m => [...m, { from: "general", text: "⚠️ Nenhum jogo ativo para analisar." }])
      return
    }
    try {
      setMessages(m => [...m, { from: "general", text: "⏳ Analisando jogada..." }])
      const res = await analyzeMove(gameId)
      setMessages(m => [
        ...m.slice(0, -1), // remove o "analisando..."
        { from: "general", text: res.analysis || res.message || JSON.stringify(res) }
      ])
    } catch (e) {
      setMessages(m => [...m, { from: "general", text: `❌ Erro: ${e.message}` }])
    }
  }

  // 🔹 Formulário: usa sendMessage
  function handleSend(e) {
    e.preventDefault()
    if (input.trim()) {
      sendMessage(input)
    }
  }

  return (
    <>
      {/* Botão fixo do General */}
      <button
        onClick={() => setOpen(o => !o)}
        className="fixed bottom-6 right-6 w-16 h-16 rounded-full shadow-lg border-2 border-white bg-neutral-900 overflow-hidden hover:scale-105 transition-transform z-50"
      >
        <img src={generalImg} alt="General" className="..." />
      </button>

      {/* Caixa de chat */}
      {open && (
        <div className="fixed bottom-24 right-6 w-80 h-96 bg-neutral-900 border border-neutral-700 rounded-xl shadow-xl flex flex-col z-50">
          {/* Header */}
          <div className="p-3 border-b border-neutral-700 flex justify-between items-center">
            <span className="font-bold text-white">General WAR</span>
            <button onClick={() => setOpen(false)} className="text-neutral-400 hover:text-white">✖</button>
          </div>

          {/* Mensagens */}
          <div className="flex-1 overflow-y-auto p-3 space-y-2 text-sm">
            {messages.map((m, i) => (
              <div
                key={i}
                className={`p-2 rounded-lg max-w-[80%] ${
                  m.from === "user"
                    ? "bg-emerald-600 text-white ml-auto"
                    : "bg-neutral-800 text-neutral-100"
                }`}
              >
                <div className="text-sm leading-relaxed whitespace-pre-wrap">
                  <ReactMarkdown>{m.text}</ReactMarkdown>
                </div>
              </div>
            ))}
          </div>

          {/* Input */}
          <form onSubmit={handleSend} className="p-3 border-t border-neutral-700 flex gap-2">
            <input
              className="flex-1 rounded-md bg-neutral-800 text-white px-2 py-1 text-sm focus:outline-none"
              placeholder="Escreva algo..."
              value={input}
              onChange={e => setInput(e.target.value)}
            />
            <button className="px-3 rounded-md bg-emerald-600 hover:bg-emerald-500 text-white text-sm">
              ➤
            </button>
          </form>

          {/* Botão extra de análise */}
          <div className="p-2 border-t border-neutral-700">
            <button
              onClick={handleAnalyze}
              className="w-full py-1 rounded-md bg-indigo-600 hover:bg-indigo-500 text-white text-sm"
            >
              📊 Analisar jogada
            </button>
          </div>
        </div>
      )}
    </>
  )
}
