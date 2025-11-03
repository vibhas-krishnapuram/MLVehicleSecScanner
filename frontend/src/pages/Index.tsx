import { Shield } from "lucide-react";
import Header from "@/components/Header";
import FileUpload from "@/components/FileUpload";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="container mx-auto px-6 py-24">
        <div className="max-w-3xl mx-auto space-y-16">
          <div className="text-center space-y-6 animate-fade-in">
            <div className="inline-flex items-center justify-center p-3 rounded-2xl bg-primary/10 mb-4">
              <Shield className="h-8 w-8 text-primary" />
            </div>
            <h1 className="text-5xl md:text-6xl font-bold text-foreground leading-tight">
              Secure Your Code with{" "}
              <span className="text-primary">AI</span>
            </h1>
            <p className="text-lg text-muted-foreground max-w-xl mx-auto leading-relaxed">
              Upload your code files and get instant vulnerability analysis with actionable recommendations
            </p>
          </div>

          <FileUpload />
        </div>
      </main>
    </div>
  );
};

export default Index;
