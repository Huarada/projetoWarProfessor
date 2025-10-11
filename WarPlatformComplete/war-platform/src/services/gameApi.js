async function req(path, opts) {
  const r = await fetch(`/api${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...opts,
  })
  if (!r.ok) throw new Error(`API ${r.status}`)
  return r.json()
}

export async function startGame() {
  return req('/game/start', {
    method: 'POST',
    body: JSON.stringify({
      auto_play: false,  // ou true, se quiser autoplay
      speed: 'normal'    // pode ser 'slow', 'normal' ou 'fast'
    })
  })
}

export async function nextTurn(gameId) {
  return req(`/game/${gameId}/next-turn`, { method: 'POST' })
}

export async function analyzeMove(gameId) {
  return req(`/game/${gameId}/analyze-move`, { method: 'POST' })
}


