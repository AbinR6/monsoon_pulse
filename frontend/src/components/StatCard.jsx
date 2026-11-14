import React from 'react';

export default function StatCard({ title, value, unit, subtitle, icon: Icon, trendBadge, color = 'cyan' }) {
  const colorMap = {
    cyan: 'border-cyan-500/30 bg-slate-900/80 text-cyan-400',
    blue: 'border-blue-500/30 bg-slate-900/80 text-blue-400',
    amber: 'border-amber-500/30 bg-slate-900/80 text-amber-400',
    emerald: 'border-emerald-500/30 bg-slate-900/80 text-emerald-400',
    violet: 'border-violet-500/30 bg-slate-900/80 text-violet-400',
    rose: 'border-rose-500/30 bg-slate-900/80 text-rose-400',
  };

  const themeClass = colorMap[color] || colorMap.cyan;

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-lg backdrop-blur-md flex flex-col justify-between hover:border-slate-700 transition">
      <div>
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs uppercase tracking-wider font-semibold text-slate-400">{title}</span>
          {Icon && (
            <div className={`p-1.5 rounded-lg border ${themeClass}`}>
              <Icon className="w-4 h-4" />
            </div>
          )}
        </div>
        <div className="flex items-baseline gap-1.5">
          <span className="text-2xl font-bold font-mono text-slate-100">{value}</span>
          {unit && <span className="text-xs text-slate-400 font-medium">{unit}</span>}
        </div>
        {subtitle && <p className="text-xs text-slate-400 mt-1">{subtitle}</p>}
      </div>

      {trendBadge && <div className="mt-3">{trendBadge}</div>}
    </div>
  );
}
