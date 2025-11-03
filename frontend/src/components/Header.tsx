import { Shield } from "lucide-react";

const Header = () => {
  return (
    <header className="border-b border-border bg-card">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center gap-2">
          <Shield className="h-6 w-6 text-primary" />
          <span className="text-xl font-semibold text-foreground">SecureCode</span>
        </div>
      </div>
    </header>
  );
};

export default Header;
