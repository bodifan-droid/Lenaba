export default function Home() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-[var(--background)] px-6">
      <div className="w-full max-w-sm space-y-8 text-center">

        {/* Temporary Logo */}

        <div className="mx-auto h-24 w-24 rounded-full bg-[var(--primary)] flex items-center justify-center text-white text-4xl font-bold shadow-lg">
          L
        </div>

        <div>
          <h1 className="text-4xl font-bold tracking-tight">
            Lenaba
          </h1>

          <p className="mt-3 text-[var(--secondary)] leading-relaxed">
            Find the one name you'll both love.
          </p>
        </div>

      </div>
    </main>
  );
}