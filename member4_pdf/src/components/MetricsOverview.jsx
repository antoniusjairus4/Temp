import React from 'react';
import { Activity, ShieldAlert, Cpu } from 'lucide-react';

export const MetricsOverview = () => {
    const metrics = [
        { title: 'Global Risk Score', value: '78/100', status: 'Moderate', color: 'text-emerald-400', icon: Activity },
        { title: 'MITRE ATT&CK Coverage', value: '64%', status: '30 Techniques Mapped', color: 'text-blue-400', icon: ShieldAlert },
        { title: 'NIST CSF Readiness', value: 'High', status: '5 Core Functions Active', color: 'text-purple-400', icon: Cpu },
    ];

    return (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            {metrics.map((item, index) => {
                const Icon = item.icon;
                return (
                    <div key={index} className="rounded-xl border border-slate-800 bg-slate-800/50 p-5 shadow-lg backdrop-blur-sm">
                        <div className="flex items-center justify-between">
                            <span className="text-sm font-medium text-slate-400">{item.title}</span>
                            <Icon className={`h-5 w-5 ${item.color}`} />
                        </div>
                        <div className="mt-3 flex items-baseline justify-between">
                            <span className="text-3xl font-extrabold text-white">{item.value}</span>
                            <span className={`text-xs font-semibold ${item.color}`}>{item.status}</span>
                        </div>
                    </div>
                );
            })}
        </div>
    );
};
