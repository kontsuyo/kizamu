import Link from "next/link";

export default function Layout({ children }: { children: React.ReactNode }) {
  const Header = () => {
    return (
      <div>
        <Link href={`/`}>
          <h1>Aging Gallery</h1>
        </Link>
      </div>
    );
  };
  return (
    <html>
      <Header />
      <body>{children}</body>
    </html>
  );
}
