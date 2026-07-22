import React from 'react';

export const DashboardGrid = () => {
    return (
        <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-3">
            {/* Slot for Member 3's Heatmap Component */}
            <div className="lg:col-span-2 rounded-xl border border-slate-800 bg-slate-800/40 p-6">
                <h2 className="text-lg font-semibold text-white mb-2">MITRE ATT&CK Heatmap Grid</h2>
                <p className="text-sm text-slate-400 mb-4">Coverage analysis mapping lab scenarios to ATT&CK techniques.</p>
                <div className="flex h-64 items-center justify-center rounded-lg border border-dashed border-slate-700 bg-slate-900/50 text-slate-500">
                    [ Member 3 Heatmap Visualization Slot ]
                </div>
            </div>

            {/* NIST Readiness Overview */}
            <div className="rounded-xl border border-slate-800 bg-slate-800/40 p-6">
                <h2 className="text-lg font-semibold text-white mb-2">NIST CSF 2.0 Functions</h2>
                <p className="text-sm text-slate-400 mb-4">Organizational readiness breakdown.</p>
                <div className="space-y-4">
                    {['Identify', 'Protect', 'Detect', 'Respond', 'Recover'].map((fn, idx) => (
                        <div key={idx} className="flex justify-between items-center text-sm">
                            <span className="text-slate-300">{fn}</span>
                            <div className="w-1/2 bg-slate-700 h-2 rounded-full overflow-hidden">
                                <div className="bg-emerald-400 h-full rounded-full" style={{ width: `${80 - idx * 8}%` }}></div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};