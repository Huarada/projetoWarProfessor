// src/components/GameBoard.jsx
import { useEffect, useMemo, useRef, useState } from 'react'
import worldMap from '@/assets/world-map.png'
import { nextTurn, analyzeMove } from '@/services/gameApi'
import COORDS from '@/constants/territoryCoords'
import { cn } from '@/lib/utils'
import GeneralChat from "@/components/GeneralChat"

export default function GameBoard({ gameId, gameState, setGameState, onExit }) {
  const [loading, setLoading] = useState(false)
  const [analysis, setAnalysis] = useState('')
  const [auto, setAuto] = useState(false)
  const [devMode, setDevMode] = useState(false)
  const containerRef = useRef(null)
  const [hover, setHover] = useState(null) // { name, x, y }

  // autoplay
  useEffect(() => {
    if (!auto) return
    let alive = true
    ;(async () => {
      while (alive && gameState && gameState.status !== 'finished') {
        setLoading(true)
        const s = await nextTurn(gameId)
        setGameState(s.state ?? s)
        setLoading(false)
        await new Promise(r => setTimeout(r, 400))
      }
    })()
    return () => { alive = false }
  }, [auto]) // eslint-disable-line

  const playersById = useMemo(() => {
    const dict = {}
    ;(gameState.players || []).forEach(p => { dict[p.id] = p })
    return dict
  }, [gameState])

  const territoryEntries = useMemo(() => {
    const t = gameState.territories || {}
    return Object.entries(t)
  }, [gameState])

  const unplaced = useMemo(() => {
    return territoryEntries
      .filter(([name]) => !COORDS[name])
      .map(([name]) => name)
      .sort()
  }, [territoryEntries])

  const last = gameState.last_action

  // pega coords em % ao clicar no mapa (Dev mode)
  function onMapClick(e) {
    if (!devMode || !containerRef.current) return
    const rect = containerRef.current.getBoundingClientRect()
    const xPct = ((e.clientX - rect.left) / rect.width) * 100
    const yPct = ((e.clientY - rect.top) / rect.height) * 100
    console.log(`{ x: ${xPct.toFixed(1)}, y: ${yPct.toFixed(1)} }`)
    alert(`Coords copiadas no console: { x: ${xPct.toFixed(1)}, y: ${yPct.toFixed(1)} }`)
  }

  return (
    <div className="max-w-[1400px] mx-auto p-4 grid grid-cols-1 lg:grid-cols-[1fr_380px] gap-6">
      {/* Coluna do mapa */}
      <section className="space-y-3">
        <div className="flex items-center gap-2">
          <ControlButton
            onClick={async () => {
              setLoading(true)
              const s = await nextTurn(gameId)
              setGameState(s.state ?? s)
              setLoading(false)
            }}
            disabled={loading || (gameState?.status === 'finished')}
            intent="primary"
          >
            Próximo turno
          </ControlButton>

          <ControlButton
            onClick={() => setAuto(v => !v)}
            disabled={gameState?.status === 'finished'}
          >
            {auto ? 'Parar auto-play' : 'Auto-play'}
          </ControlButton>

          <ControlButton
            onClick={async () => {
              try {
                const res = await analyzeMove(gameId)
                setAnalysis(res.analysis || res.message || JSON.stringify(res))
              } catch (e) {
                setAnalysis(String(e?.message || e))
              }
            }}
            intent="indigo"
          >
            Analisar jogada
          </ControlButton>

          <div className="ml-auto flex items-center gap-2">
            <label className="text-sm opacity-80 select-none">
              <input
                type="checkbox"
                className="align-middle mr-2"
                checked={devMode}
                onChange={e => setDevMode(e.target.checked)}
              />
              Dev mode (pegar coordenadas)
            </label>

            <ControlButton onClick={onExit}>Sair do jogo</ControlButton>
          </div>
        </div>

        {/* MAPA */}
        <div
          ref={containerRef}
          className={cn(
            'relative w-full rounded-xl overflow-hidden border',
            'border-neutral-700 bg-neutral-950'
          )}
          onClick={onMapClick}
        >
          <img
            src={worldMap}
            alt="Mapa WAR"
            className="w-full h-auto block opacity-95"
            draggable={false}
          />
          

          {/* Marcadores de territórios */}
          {territoryEntries.map(([name, info]) => {
            const coords = COORDS[name]
            if (!coords) return null
            const owner = playersById[info.dono]
            const color = owner?.color || '#999'

            return (
              <Marker
                key={name}
                name={name}
                troops={info.tropas}
                color={color}
                style={{
                  left: `${coords.x}%`,
                  top: `${coords.y}%`,
                }}
                onHover={setHover}
              />
            )
          })}

          {/* Tooltip */}
          {hover && (
          <div
            className="pointer-events-none absolute z-30 bg-black/80 text-white text-xs rounded px-2 py-1 border border-white/10 shadow"
            style={{
              left: hover.x - 400, // um pouco à direita do cursor
              top: hover.y - 100,  // um pouco acima do cursor
            }}
          >
              <div className="font-semibold">{hover.name}</div>
              <div>Tropas: {hover.troops}</div>
            </div>
          )}
        </div>
      </section>

      {/* Painel lateral */}
      <aside className="space-y-3">
        <Panel title="Estado do Jogo">
          <div className="text-sm grid grid-cols-2 gap-y-1">
            <div className="opacity-80">Rodada</div><div>{gameState.current_round}</div>
            <div className="opacity-80">Jogador atual</div><div>{gameState.current_player}</div>
            <div className="opacity-80">Status</div><div>{gameState.status}</div>
            <div className="opacity-80">Turnos</div><div>{gameState.total_turns}</div>
          </div>
        </Panel>

        <Panel title="Jogadores">
          <ul className="space-y-2">
            {(gameState.players || []).map(p => (
              <li key={p.id} className="flex items-center gap-2">
                <span className="inline-block size-3 rounded-full" style={{ background: p.color }} />
                <span className={cn('font-medium', p.eliminated && 'line-through opacity-60')}>
                  #{p.id} — gene {p.gene}
                </span>
                <span className="ml-auto text-xs opacity-80">
                  Territórios: {p.territories_count} · Tropas: {p.total_troops}
                </span>
              </li>
            ))}
          </ul>
        </Panel>

        {last && (
          <Panel title="Última ação">
            <div className="text-sm">
              {last.type === 'attack' ? (
                <>
                  <div><b>Jogador:</b> {last.player}</div>
                  <div><b>De:</b> {last.from}</div>
                  <div><b>Para:</b> {last.to}</div>
                  <div><b>Sucesso:</b> {last.success ? 'sim' : 'não'}</div>
                </>
              ) : (
                <div>Sem ataque (motivo: {last.reason})</div>
              )}
              {'winner' in last && (
                <div className="mt-2 text-emerald-400 font-semibold">🏆 Vencedor: jogador {last.winner}</div>
              )}
            </div>
          </Panel>
        )}

        {!!analysis && (
          <Panel title="Análise do Chatbot">
            <p className="text-sm leading-relaxed whitespace-pre-wrap">{analysis}</p>
          </Panel>
        )}

        {unplaced.length > 0 && (
          <Panel title="Sem posição (adicione em territoryCoords.js)">
            <ul className="text-xs space-y-1 opacity-80">
              {unplaced.map(n => <li key={n}>{n}</li>)}
            </ul>
          </Panel>
        )}


        {/* Lista de territórios e donos */}
          <Panel title="Territórios e Donos">
            <ul className="max-h-[400px] overflow-y-auto space-y-1 text-sm">
              {territoryEntries.map(([name, info]) => {
                const owner = playersById[info.dono]
                return (
                  <li key={name} className="flex items-center gap-2">
                    <span className="font-medium">{name}</span>
                    <span className="text-xs opacity-70">({info.tropas} tropas)</span>
                    {owner && (
                      <span className="ml-auto flex items-center gap-1">
                        <span
                          className="inline-block size-3 rounded-full"
                          style={{ background: owner.color }}
                        />
                        <span className="text-xs">
                          Jogador #{owner.id} ({owner.strategy})
                        </span>
                      </span>
                    )}
                  </li>
                )
              })}
            </ul>
          </Panel>


      </aside>
      {/* Chat do General fixo no canto inferior direito */}
      <GeneralChat gameId={gameId} />

    </div>
    
  )
}

/* ---------- componentes UI locais ---------- */

function ControlButton({ intent = 'neutral', className = '', ...props }) {
  const styles = {
    primary: 'bg-emerald-600 hover:bg-emerald-500 text-white',
    indigo: 'bg-indigo-600 hover:bg-indigo-500 text-white',
    neutral:
      'border border-neutral-600 hover:bg-neutral-800 text-neutral-200',
  }[intent] || 'border border-neutral-600 hover:bg-neutral-800 text-neutral-200'
  return (
    <button
      className={cn(
        'px-3 py-1 rounded-md text-sm transition-colors',
        styles,
        className
      )}
      {...props}
    />
  )
}

function Panel({ title, children }) {
  return (
    <div className="bg-neutral-900/60 border border-neutral-700 rounded-xl p-3">
      <h4 className="font-semibold mb-2 text-neutral-100">{title}</h4>
      {children}
    </div>
  )
}

function Marker({ name, troops, color, style, onHover }) {
  return (
    <div
      className="absolute z-20 -translate-x-1/2 -translate-y-1/2"
      style={style}
onMouseEnter={e => {
  const rect = e.currentTarget.getBoundingClientRect()
  onHover?.({
    name,
    troops,
    x: e.clientX,
    y: e.clientY,
  })
}}
onMouseMove={e => {
  onHover?.({
    name,
    troops,
    x: e.clientX,
    y: e.clientY,
  })
}}
      onMouseLeave={() => onHover?.(null)}
    >
      <div
        className="rounded-full grid place-items-center"
        style={{
          background: color,       // agora usa a cor do jogador
          width: 30,
          height: 30,
          border: "2px solid white",
          boxShadow: '0 4px 12px rgba(0,0,0,.4)',
        }}
      >
        <span className="text-[12px] font-semibold text-white select-none">
          {troops}
        </span>
      </div>
    </div>
  )
}
