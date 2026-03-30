interface ScoreCardProps {
  finalScore: number | null;
  didPass: boolean | null;
}

export default function ScoreCard({ finalScore, didPass }: ScoreCardProps) {
  if (finalScore === null || didPass === null) {
    return null;
  }

  return (
    <div className="score-card">
      <h4>Final Result</h4>
      <p className="score-line">
        Score: <strong>{finalScore.toFixed(2)} / 50.00</strong>
      </p>
      <p
        className={`pass-fail-pill ${
          didPass ? "pass-fail-pass" : "pass-fail-fail"
        }`}
      >
        {didPass ? "Pass" : "Fail"}
      </p>
    </div>
  );
}
