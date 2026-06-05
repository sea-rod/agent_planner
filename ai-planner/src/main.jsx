import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router';
import './index.css'
import App from './pages/App.jsx'
import AuthPage from './pages/AuthPage.jsx'
import Layout from './components/layouts.jsx';
import ChatPage from './pages/ChatPage.jsx';
import Terms from "./pages/Terms.jsx";
import Privacy from "./pages/Privacy.jsx"
import Connector from './pages/Connector.jsx';
import WaitlistPage from './pages/WaitlistPage.jsx';


const router = createBrowserRouter([
  {
    // The Layout is the parent; it contains the Navbar and Footer
    path: "/",
    element: <Layout />,
    children: [
      {
        // This is the default page (index) when you are at "/"
        index: true,
        element: <App />,
      },
      {
        // This is the page at "/auth"
        path: "auth",
        element: <AuthPage />,
      },
      {
        path: "chat",
        element: <ChatPage />
      },
      {
        path: "connector",
        element: <Connector />
      },
      {
        path: "terms",
        element: <Terms />
      },
      {
        path: "privacy",
        element: <Privacy />
      },
      {
        path: "waitlist",
        element: <WaitlistPage />
      },
    ],
  },
]);

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
