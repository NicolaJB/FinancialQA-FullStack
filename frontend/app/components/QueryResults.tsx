interface Props {
  results: string[];
}

export default function QueryResults({ results }: Props) {
  if (!results.length) return null;
  return (
    <div className="space-y-4">
      {results.map((res, idx) => (
        <div key={idx} className="p-4 bg-white rounded shadow">
          {res}
        </div>
      ))}
    </div>
  );
}
