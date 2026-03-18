import { useParams } from "react-router-dom";
import { InterviewPageEditor } from "@/features/interview";
import { ProblemWorkspace } from "@/features/problem";
import type { Problem } from "@/types/problem";

export default function InterviewPage() {
  const { id } = useParams();

  return (
    <ProblemWorkspace
      problemId={id ?? ""}
      splitDefaultPrimarySize={30}
      splitMinPrimarySize={22}
      splitMaxPrimarySize={55}
      secondaryComponent={(problem: Problem) => (
        <InterviewPageEditor problem={problem} />
      )}
    />
  );
}
