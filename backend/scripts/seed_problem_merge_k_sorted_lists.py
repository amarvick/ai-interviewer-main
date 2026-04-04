"""
Seed script for the "Merge k Sorted Lists" problem.

Run:
    python scripts/seed_problem_merge_k_sorted_lists.py
"""

from pathlib import Path
import sys

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db.database import Base, SessionLocal, engine
from app.db.models import Problem, ProblemList, ProblemListProblem
import app.db.models  # noqa: F401


REFERENCE_VARIANTS = [
    {
        "id": "min_heap_merge",
        "title": "Min-heap merge (optimal)",
        "pseudocode": """1. Push head of each non-empty list into min-heap (value, idx, node)
2. While heap not empty:
       val, idx, node = heappop
       append node to result
       if node.next: heappush(node.next)
3. Return merged list head
Time: O(N log k) where N is total nodes. Space: O(k).""",
        "complexity": "O(N log k) time, O(k) space",
        "is_optimal": True,
        "notes": "Maintains heap of k heads; handles up to 10^4 total nodes efficiently.",
        "match_signals": [
            "heapq",
            "priority queue",
            "O(N log k)",
        ],
        "strengths": [
            "Works well when k is large and lists lengths vary.",
        ],
        "improvements": [
            "Mention tie-breaking (e.g., using index) to keep heap entries comparable.",
        ],
    },
    {
        "id": "divide_and_conquer_merge",
        "title": "Pairwise divide-and-conquer",
        "pseudocode": """Repeatedly merge lists in pairs (similar to merge sort) until one remains.
Time: O(N log k). Space: O(1) apart from recursion stack.""",
        "complexity": "O(N log k) time, O(1) extra space",
        "is_optimal": True,
        "notes": "Good alternative that reuses two-list merge logic.",
        "match_signals": [
            "mergeTwoLists",
            "divide and conquer",
        ],
        "strengths": [
            "Avoids heap overhead when merges are easy to implement.",
        ],
        "improvements": [
            "Clarify recursion depth or iterative pairing to avoid stack overflow.",
        ],
    },
    {
        "id": "flatten_then_sort",
        "title": "Flatten all nodes then sort",
        "pseudocode": """Collect all values, sort, rebuild list.
Time: O(N log N).""",
        "complexity": "O(N log N) time, O(N) space",
        "is_optimal": False,
        "notes": "Simple but exceeds O(N log k) when k << N.",
        "match_signals": [
            "array of values",
            "sorted(values)",
        ],
        "strengths": [
            "Easy to code for quick prototypes.",
        ],
        "improvements": [
            "Explain inefficiency when k is small relative to N.",
        ],
    },
]

REFERENCE_TALKING_POINTS = [
    {
        "id": "complexity_goal",
        "title": "Why O(N log k)",
        "description": "Highlight that merging k lists one node at a time costs log k per extraction, leading to O(N log k).",
        "bonus_mentions": [
            "N = total nodes <= 1e4",
            "heap size k",
        ],
    },
    {
        "id": "data_structure_choice",
        "title": "Choosing heap vs divide-and-conquer",
        "description": "Discuss trade-offs between maintaining a priority queue and recursively merging pairs.",
        "bonus_mentions": [
            "memory footprint",
            "cache locality",
        ],
    },
]

MERGE_K_LISTS = {
    "slug": "merge-k-sorted-lists",
    "title": "Merge k Sorted Lists",
    "category": "Linked Lists",
    "difficulty": "Hard",
    "description": """You are given an array of `k` linked lists, each sorted in ascending order. Merge all the linked lists into one sorted list and return its head.

Example 1
```
Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
```

Example 2
```
Input: lists = []
Output: []
```

Example 3
```
Input: lists = [[]]
Output: []
```

Constraints
- `0 <= k <= 10^4`
- `0 <= lists[i].length <= 500`
- Total number of nodes across all lists <= 10^4
- `-10^4 <= lists[i][j] <= 10^4`
- Each list is sorted in ascending order.
""",
    "starter_code": {
        "python": """# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        # Write your code here
        return None
""",
        "javascript": """/**
 * Definition for singly-linked list.
 * function ListNode(val, next) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.next = (next===undefined ? null : next)
 * }
 */
class Solution {
  /**
   * @param {ListNode[]} lists
   * @return {ListNode}
   */
  mergeKLists(lists) {
    // Write your code here
    return null;
  }
}

module.exports = { Solution };
""",
        "java": """/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public ListNode mergeKLists(ListNode[] lists) {
        // Write your code here
        return null;
    }
}
""",
        "cpp": """/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        // Write your code here
        return nullptr;
    }
};
""",
    },
    "reference_pseudocode": """Use a min-heap for all list heads:

1. Push (value, unique_id, node) for each non-null list head.
2. Initialize dummy head and tail pointer.
3. While heap not empty:
       val, _, node = heappop
       tail.next = node
       tail = tail.next
       if node.next:
           heappush(node.next)
4. Return dummy.next
""",
    "reference_pseudocode_variants": REFERENCE_VARIANTS,
    "reference_talking_points": REFERENCE_TALKING_POINTS,
}

TARGET_LIST_IDS = (
    "blind_75",
    "taro_75",
    "neetcode_150",
    "grind_169",
    "google_50",
)


def seed_merge_k_lists() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        problem = (
            db.query(Problem)
            .filter(Problem.slug == MERGE_K_LISTS["slug"])
            .first()
        )
        if problem is None:
            problem = (
                db.query(Problem)
                .filter(Problem.title == MERGE_K_LISTS["title"])
                .first()
            )

        if problem is None:
            problem = Problem(
                slug=MERGE_K_LISTS["slug"],
                title=MERGE_K_LISTS["title"],
                description=MERGE_K_LISTS["description"],
                difficulty=MERGE_K_LISTS["difficulty"],
                category=MERGE_K_LISTS["category"],
                starter_code=MERGE_K_LISTS["starter_code"],
                reference_pseudocode=MERGE_K_LISTS["reference_pseudocode"],
                reference_pseudocode_variants=MERGE_K_LISTS["reference_pseudocode_variants"],
                reference_talking_points=MERGE_K_LISTS["reference_talking_points"],
            )
            db.add(problem)
            db.flush()
            print("Inserted problem: Merge k Sorted Lists")
        else:
            problem.description = MERGE_K_LISTS["description"]
            problem.difficulty = MERGE_K_LISTS["difficulty"]
            problem.category = MERGE_K_LISTS["category"]
            problem.starter_code = MERGE_K_LISTS["starter_code"]
            problem.reference_pseudocode = MERGE_K_LISTS["reference_pseudocode"]
            problem.reference_pseudocode_variants = MERGE_K_LISTS["reference_pseudocode_variants"]
            problem.reference_talking_points = MERGE_K_LISTS["reference_talking_points"]
            problem.slug = MERGE_K_LISTS["slug"]
            db.flush()
            print("Updated problem: Merge k Sorted Lists")

        linked = skipped = 0
        for list_id in TARGET_LIST_IDS:
            problem_list = db.query(ProblemList).filter(ProblemList.id == list_id).first()
            if problem_list is None:
                continue
            existing_link = (
                db.query(ProblemListProblem)
                .filter(
                    ProblemListProblem.problem_list_id == list_id,
                    ProblemListProblem.problem_id == problem.id,
                )
                .first()
            )
            if existing_link:
                skipped += 1
                continue
            db.add(ProblemListProblem(problem_list_id=list_id, problem_id=problem.id))
            linked += 1

        db.commit()
        print(f"Done. Linked to lists: {linked}, Existing links skipped: {skipped}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_merge_k_lists()
