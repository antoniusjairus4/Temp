import React from 'react';
import { ShieldCheck } from 'lucide-react';
import { DownloadPDFButton } from './ExecutivePDF';

export const Header = () => {
    return (
        <header className="border-b border-slate-800 bg-slate-900/80 px-6 py-4 backdrop-blur-md flex items-center justify-between">
            <div className="flex items-center space-x-3">
                <ShieldCheck className="h-8 w-8 text-emerald-400" />
                <div>
                    <h1 className="text-xl font-bold tracking-tight text-white">PWNDORA</h1>
                    <p className="text-xs text-slate-400">RiskView360 | CISO Posture Intelligence</p>
                </div>
            </div>
            <DownloadPDFButton />
        </header>
    );
};