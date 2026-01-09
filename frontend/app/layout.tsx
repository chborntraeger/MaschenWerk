import Footer from "@/components/Footer";
import Header from "@/components/Header";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Knitting Projects",
  description: "Personal knitting project showcase and pattern library",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark:bg-gray-900">
      <body className={`${inter.className} flex flex-col min-h-screen bg-slate-100 dark:bg-slate-900`}>
        <Header />
        <main className="flex-1 bg-slate-100 dark:bg-slate-900">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
