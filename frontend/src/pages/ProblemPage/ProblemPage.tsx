import { useParams } from "react-router-dom";
import { ProblemWorkspace, ProblemPageEditor } from "@/features/problem";
import type { Problem } from "@/types/problem";

export default function ProblemPage() {
  const { id } = useParams();

  return (
    <ProblemWorkspace
      problemId={id ?? ""}
      secondaryComponent={(problem: Problem) => (
        <ProblemPageEditor problem={problem} />
      )}
    />
  );
}
