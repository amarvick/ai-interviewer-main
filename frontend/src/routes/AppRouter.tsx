// routes/AppRouter.tsx
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Layout from "../components/Layout/Layout";
import HomePage from "../pages/HomePage/HomePage";
import LoginPage from "../pages/LoginPage/LoginPage";
import SignupPage from "../pages/SignupPage/SignupPage";
import ProblemListPage from "../pages/ProblemListPage/ProblemListPage";
import ProblemPage from "../pages/ProblemPage/ProblemPage";
import InterviewPage from "../pages/InterviewPage/InterviewPage";

const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      { path: "/", element: <HomePage /> },
      { path: "/login", element: <LoginPage /> },
      { path: "/signup", element: <SignupPage /> },
      { path: "/list/:id", element: <ProblemListPage /> },
      { path: "/problem/:slug", element: <ProblemPage /> },
      { path: "/interview-problem/:slug", element: <InterviewPage /> },
    ],
  },
]);

export default function AppRouter() {
  return <RouterProvider router={router} />;
}
