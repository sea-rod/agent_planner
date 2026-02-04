import { Outlet } from 'react-router';
import Navbar from './navbar';
import Footer from './footer'

const Layout = () => {
  return (
    <div className="min-h-screen bg-primary">
      <Navbar/>
      {/* This Outlet is where LandingPage or AuthPage will appear */}
      <main>
        <Outlet />
      </main>
     <Footer/>
    </div>
  );
};

export default Layout;