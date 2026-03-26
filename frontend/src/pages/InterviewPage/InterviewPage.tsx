import { useParams } from "react-router-dom";
import { InterviewPageEditor } from "@/features/interview";
import { ProblemWorkspace } from "@/features/problem";
import type { Problem } from "@/types/problem";

export default function InterviewPage() {
  const { slug } = useParams();

  return (
    <ProblemWorkspace
      problemSlug={slug ?? ""}
      splitDefaultPrimarySize={30}
      splitMinPrimarySize={22}
      splitMaxPrimarySize={55}
      secondaryComponent={(problem: Problem) => (
        <InterviewPageEditor problem={problem} />
      )}
    />
  );
}
