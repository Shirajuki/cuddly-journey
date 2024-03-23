import Footer from "@/components/layout/Footer";
import Navigation from "@/components/layout/Navigation";
import { createRootRoute, Outlet } from "@tanstack/react-router";
// import { TanStackRouterDevtools } from "@tanstack/router-devtools";

export const Route = createRootRoute({
  component: () => (
    <>
      <Navigation />
      <main className="dark bg-background text-foreground min-h-screen overflow-hidden p-4 max-w-screen-2xl mx-auto pt-20">
        <Outlet />
      </main>
      <Footer />
      {/* <TanStackRouterDevtools /> */}
    </>
  ),
});
