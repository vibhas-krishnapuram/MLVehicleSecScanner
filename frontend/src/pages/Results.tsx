import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { RefreshCw, FileCode } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import VulnerabilityCard from "@/components/VulnerabilityCard";
import Header from "@/components/Header";
import { useToast } from "@/hooks/use-toast";

interface Vulnerability {
  type: string;
  severity: "High" | "Medium" | "Low";
  example: string;
  recommended_fix: string;
  code_to_fix: string;
  line_number: number;
}

interface ScanResults {
  findings: Vulnerability[];
}

const Results = () => {
  const { filename } = useParams();
  const navigate = useNavigate();
  const { toast } = useToast();
  const [results, setResults] = useState<ScanResults | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchResults = async () => {
      if (!filename) return;

      try {
        const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
        const response = await fetch(`${apiUrl}/responses/${filename}`);
        
        if (!response.ok) {
          throw new Error("Failed to fetch results");
        }

        const data = await response.json();
        
        // Backend returns array directly, wrap it in findings object
        // Also normalize field names to match our interface
        const normalizedData = {
          findings: Array.isArray(data) ? data.map((item: any) => ({
            type: item.type,
            severity: item.severity,
            example: item.example || item.real_world_example || "",
            recommended_fix: item.recommended_fix,
            code_to_fix: item.code_to_fix || item.code || "",
            line_number: item.line_number || item.line || 0
          })) : []
        };
        
        setResults(normalizedData);
      } catch (error) {
        toast({
          title: "Error",
          description: "Failed to load scan results",
          variant: "destructive",
        });
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
  }, [filename, toast]);

  const highCount = results?.findings?.filter((f) => f.severity === "High").length || 0;
  const mediumCount = results?.findings?.filter((f) => f.severity === "Medium").length || 0;
  const lowCount = results?.findings?.filter((f) => f.severity === "Low").length || 0;
  const totalCount = results?.findings?.length || 0;

  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <Header />
        <div className="container mx-auto px-6 py-12 flex items-center justify-center">
          <div className="text-center space-y-4">
            <RefreshCw className="h-12 w-12 text-primary animate-spin mx-auto" />
            <p className="text-lg text-muted-foreground">Loading scan results...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <div className="container mx-auto px-6 py-12">
        <div className="max-w-4xl mx-auto space-y-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 animate-fade-in">
            <div>
              <h1 className="text-3xl font-bold text-foreground mb-2">
                Found {totalCount} vulnerabilit{totalCount === 1 ? "y" : "ies"} in{" "}
                <span className="text-primary">{filename}</span>
              </h1>
              <div className="flex gap-2 flex-wrap">
                {highCount > 0 && (
                  <Badge variant="destructive">{highCount} High</Badge>
                )}
                {mediumCount > 0 && (
                  <Badge variant="warning">{mediumCount} Medium</Badge>
                )}
                {lowCount > 0 && (
                  <Badge variant="default">{lowCount} Low</Badge>
                )}
              </div>
            </div>
            <Button
              onClick={() => navigate("/")}
              variant="outline"
              className="gap-2"
            >
              <RefreshCw className="h-4 w-4" />
              Scan Another File
            </Button>
          </div>

          {results?.findings && results.findings.length > 0 ? (
            <div className="space-y-6">
              {results.findings.map((finding, index) => (
                <VulnerabilityCard
                  key={index}
                  type={finding.type}
                  severity={finding.severity}
                  example={finding.example}
                  recommendedFix={finding.recommended_fix}
                  codeToFix={finding.code_to_fix}
                  lineNumber={finding.line_number}
                />
              ))}
            </div>
          ) : (
            <div className="text-center py-12 bg-card rounded-lg border border-border">
              <FileCode className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-lg text-foreground font-medium">No vulnerabilities found</p>
              <p className="text-sm text-muted-foreground mt-1">Your code looks secure!</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Results;
