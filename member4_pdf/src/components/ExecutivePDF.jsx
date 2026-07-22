import React from 'react';
import { Document, Page, Text, View, StyleSheet, PDFDownloadLink } from '@react-pdf/renderer';

const styles = StyleSheet.create({
    page: { padding: 40, backgroundColor: '#FFFFFF', fontFamily: 'Helvetica' },
    header: { borderBottomWidth: 2, borderBottomColor: '#0f172a', paddingBottom: 10, marginBottom: 20 },
    title: { fontSize: 20, color: '#0f172a', fontWeight: 'bold' },
    subtitle: { fontSize: 10, color: '#64748b' },
    card: { backgroundColor: '#f8fafc', padding: 15, borderRadius: 5, marginBottom: 15 },
    cardTitle: { fontSize: 14, fontWeight: 'bold', color: '#1e293b', marginBottom: 5 },
    metric: { fontSize: 28, fontWeight: 'bold', color: '#10b981' },
    bodyText: { fontSize: 10, color: '#334155', lineHeight: 1.5, marginBottom: 8 }
});

const MyDocument = ({ data }) => (
    <Document>
        {/* PAGE 1: Executive Summary */}
        <Page size="A4" style={styles.page}>
            <View style={styles.header}>
                <Text style={styles.title}>PWNDORA | Executive Risk Report</Text>
                <Text style={styles.subtitle}>Generated for CISO & Board Review</Text>
            </View>

            <View style={styles.card}>
                <Text style={styles.cardTitle}>Global Risk Score</Text>
                <Text style={styles.metric}>{data?.score || 78}/100</Text>
                <Text style={styles.bodyText}>Calculated using weighted NIST CSF functions and active MITRE technique coverage.</Text>
            </View>

            <View style={styles.card}>
                <Text style={styles.cardTitle}>NIST CSF Summary</Text>
                <Text style={styles.bodyText}>• Identify: 80% Readiness</Text>
                <Text style={styles.bodyText}>• Protect: 72% Readiness</Text>
                <Text style={styles.bodyText}>• Detect: 64% Readiness</Text>
            </View>
        </Page>

        {/* PAGE 2: Actionable Recommendations */}
        <Page size="A4" style={styles.page}>
            <View style={styles.header}>
                <Text style={styles.title}>Actionable Remediation Strategy</Text>
                <Text style={styles.subtitle}>Prioritized Defensive Upgrades</Text>
            </View>

            <View style={styles.card}>
                <Text style={styles.cardTitle}>High Priority Focus Areas</Text>
                <Text style={styles.bodyText}>1. Expand Credential Access defense lab simulations.</Text>
                <Text style={styles.bodyText}>2. Strengthen API endpoint validation on public services.</Text>
            </View>
        </Page>
    </Document>
);

export const DownloadPDFButton = () => (
    <PDFDownloadLink
        document={<MyDocument data={{ score: 78 }} />}
        fileName="PWNDORA_Executive_Summary.pdf"
        className="rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 transition hover:bg-emerald-400 shadow-md"
    >
        {({ loading }) => (loading ? 'Generating Report...' : 'Download Executive PDF')}
    </PDFDownloadLink>
);