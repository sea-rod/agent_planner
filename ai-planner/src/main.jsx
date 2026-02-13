import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router';
import './index.css'
import App from './pages/App.jsx'
import AuthPage from './pages/AuthPage.jsx'
import Layout from './components/layouts.jsx';
import ChatPage from './pages/ChatPage.jsx';


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
    ],
  },
]);

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
