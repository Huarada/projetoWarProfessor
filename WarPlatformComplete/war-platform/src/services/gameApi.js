async function req(path, opts) {
  const r = await fetch(`/api${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...opts,
  })
  if (!r.ok) throw new Error(`API ${r.status}`)
  return r.json()
}

// nova versão genérica do startGame
export const startGame = (opts = {}) =>
  req('/game/start', {
    method: 'POST',
    body: JSON.stringify({
      auto_play: false,
      speed: 'normal',
      ...opts   // ← isso permite incluir parâmetros extras, como include_human: true
    }),
  })


// helper: ação do jogador humano (deploy, attack, fortify)
export const playerAction = (game_id, action, params) =>
  req('/player/action', {
    method: 'POST',
    body: JSON.stringify({ game_id, action, params }),
  })

// helper: encerrar turno do humano
export const endTurn = (game_id) =>
  req('/player/end-turn', {
    method: 'POST',
    body: JSON.stringify({ game_id }),
  })



export async function nextTurn(gameId) {
  return req(`/game/${gameId}/next-turn`, { method: 'POST' })
}

export async function analyzeMove(gameId) {
  return req(`/game/${gameId}/analyze-move`, { method: 'POST' })
}


