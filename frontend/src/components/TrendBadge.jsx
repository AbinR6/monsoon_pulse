import React from 'react';
import { TrendingUp, TrendingDown, Minus, CheckCircle, AlertTriangle } from 'lucide-react';

export default function TrendBadge({ trend, pValue, qValue, slope, unit, compact = false }) {
  let isSig = false;
  let isFdr = false;

  if (pValue !== undefined && pValue !== null) {
    isSig = pValue < 0.05;
  }
  if (qValue !== undefined && qValue !== null) {
    isFdr = qValue < 0.05;
  }

  const isIncreasing = trend === 'Increasing';
  const isDecreasing = trend === 'Decreasing';

  let colorClasses = 'bg-slate-800 text-slate-300 border-slate-700';
  if (isIncreasing) {
    colorClasses = isFdr ? 'bg-rose-950/70 text-rose-300 border-rose-700/60' : 'bg-amber-950/60 text-amber-300 border-amber-700/50';
  } else if (isDecreasing) {
    colorClasses = isFdr ? 'bg-emerald-950/70 text-emerald-300 border-emerald-700/60' : 'bg-teal-950/60 text-teal-300 border-teal-700/50';
  }

  if (compact) {
    return (
      <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium border ${colorClasses}`}>
        {isIncreasing && <TrendingUp className="w-3 h-3 text-rose-400" />}
        {isDecreasing && <TrendingDown className="w-3 h-3 text-emerald-400" />}
        {!isIncreasing && !isDecreasing && <Minus className="w-3 h-3 text-slate-400" />}
        <span>{trend}</span>
      </span>
    );
  }

  return (
    <div className={`p-2.5 rounded-lg border text-xs ${colorClasses} flex flex-col gap-1`}>
      <div className="flex items-center justify-between font-semibold">
        <span className="flex items-center gap-1.5">
          {isIncreasing && <TrendingUp className="w-4 h-4 text-rose-400" />}
          {isDecreasing && <TrendingDown className="w-4 h-4 text-emerald-400" />}
          {!isIncreasing && !isDecreasing && <Minus className="w-4 h-4 text-slate-400" />}
          {trend}
        </span>
        {isFdr ? (
          <span className="inline-flex items-center gap-1 text-[10px] uppercase tracking-wider bg-emerald-500/20 text-emerald-300 px-1.5 py-0.5 rounded border border-emerald-500/30">
            <CheckCircle className="w-2.5 h-2.5" /> FDR Sig
          </span>
        ) : isSig ? (
          <span className="inline-flex items-center gap-1 text-[10px] uppercase tracking-wider bg-amber-500/20 text-amber-300 px-1.5 py-0.5 rounded border border-amber-500/30">
            <AlertTriangle className="w-2.5 h-2.5" /> Unadj Sig
          </span>
        ) : (
          <span className="text-[10px] text-slate-400">p ≥ 0.05</span>
        )}
      </div>

      {slope !== undefined && slope !== null && (
        <div className="flex items-center justify-between text-slate-300 font-mono mt-0.5">
          <span>Slope:</span>
          <span>{slope > 0 ? `+${slope}` : slope} {unit}</span>
        </div>
      )}

      {pValue !== undefined && pValue !== null && (
        <div className="flex items-center justify-between text-slate-400 text-[11px]">
          <span>p = {pValue}</span>
          {qValue !== undefined && qValue !== null && <span>q = {qValue}</span>}
        </div>
      )}
    </div>
  );
}
