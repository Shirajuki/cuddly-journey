import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";
import { cn } from "@/lib/utils";
import { Link } from "@tanstack/react-router";

const navigationMenuItems = [
  {
    label: "Home",
    href: "/",
  },
  {
    label: "Playground",
    href: "/playground",
  },
  {
    label: "Editor",
    href: "/editor",
  },
  {
    label: "Batch edit",
    href: "/batch-edit",
  },
  {
    label: "Documentation",
    href: "/documentation",
  },
];
export default function Navigation() {
  return (
    <header className="dark text-foreground fixed top-0 z-50 w-full border-b border-border/40 backdrop-blur-lg max-w-screen-2xl mx-auto left-0 h-16 bg-neutral-800/20 justify-center px-3 items-center rounded-b-sm flex overflow-hidden">
      <NavigationMenu className="container flex h-14 max-w-screen-2xl items-center gap-2">
        <NavigationMenuList className="hidden md:flex">
          {navigationMenuItems.map((item) => (
            <NavigationMenuItem key={item.href}>
              <Link to={item.href} className={cn(navigationMenuTriggerStyle(), "[&.active]:bg-accent/80")}>
                {item.label}
              </Link>
            </NavigationMenuItem>
          ))}
        </NavigationMenuList>
      </NavigationMenu>
    </header>
  );
}
