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
    <header className="dark bg-background text-foreground sticky top-0 z-50 w-full border-b border-border/40 backdrop-blur max-w-screen-2xl mx-auto">
      <NavigationMenu className="container flex h-14 max-w-screen-2xl items-center gap-2">
        <NavigationMenuList className="hidden md:flex">
          {navigationMenuItems.map((item) => (
            <NavigationMenuItem key={item.href}>
              <Link to={item.href} className={cn(navigationMenuTriggerStyle(), "[&.active]:bg-accent/50")}>
                {item.label}
              </Link>
            </NavigationMenuItem>
          ))}
        </NavigationMenuList>
      </NavigationMenu>
    </header>
  );
}
