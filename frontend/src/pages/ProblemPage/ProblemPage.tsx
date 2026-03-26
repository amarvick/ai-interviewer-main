import { useParams } from "react-router-dom";
import { ProblemWorkspace, ProblemPageEditor } from "@/features/problem";
import type { Problem } from "@/types/problem";

export default function ProblemPage() {
  const { slug } = useParams();

  return (
    <ProblemWorkspace
      problemSlug={slug ?? ""}
      secondaryComponent={(problem: Problem) => (
        <ProblemPageEditor problem={problem} />
      )}
    />
  );
}
