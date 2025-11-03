import { useState } from "react";
import { Upload, FileCode } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { useNavigate } from "react-router-dom";

const FileUpload = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const { toast } = useToast();
  const navigate = useNavigate();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleUpload = async () => {
    if (!file) {
      toast({
        title: "No file selected",
        description: "Please select a file to scan",
        variant: "destructive",
      });
      return;
    }

    setIsUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const response = await fetch(`${apiUrl}/upload/`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Upload failed");

      const data = await response.json();
      
      toast({
        title: "Success!",
        description: "File uploaded and scanned successfully",
      });

      // Navigate to results page with full filename
      navigate(`/results/${file.name}`);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to upload and scan file",
        variant: "destructive",
      });
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="w-full max-w-xl mx-auto space-y-6 animate-fade-in">
      <div
        className={`border-2 border-dashed rounded-xl p-12 text-center transition-all duration-200 ${
          isDragging
            ? "border-primary bg-primary/5 scale-105"
            : "border-border bg-card hover:border-primary/50"
        }`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        <div className="flex flex-col items-center gap-4">
          <div className="p-4 rounded-full bg-primary/10">
            <Upload className="h-8 w-8 text-primary" />
          </div>
          <div>
            <p className="text-lg font-medium text-foreground mb-1">
              Drop your code file here
            </p>
            <p className="text-sm text-muted-foreground">
              or click to browse
            </p>
          </div>
          <input
            type="file"
            onChange={handleFileChange}
            className="hidden"
            id="file-upload"
            accept=".c,.cpp,.py,.js,.ts,.java,.go,.rs"
          />
          <label htmlFor="file-upload">
            <Button variant="outline" className="cursor-pointer" asChild>
              <span>Browse Files</span>
            </Button>
          </label>
        </div>
      </div>

      {file && (
        <div className="flex items-center justify-between p-4 bg-card rounded-lg border border-border animate-scale-in">
          <div className="flex items-center gap-3">
            <FileCode className="h-5 w-5 text-primary" />
            <div>
              <p className="text-sm font-medium text-foreground">{file.name}</p>
              <p className="text-xs text-muted-foreground">
                {(file.size / 1024).toFixed(2)} KB
              </p>
            </div>
          </div>
          <Button
            onClick={handleUpload}
            disabled={isUploading}
            className="bg-primary hover:bg-primary/90"
          >
            {isUploading ? "Scanning..." : "Scan File"}
          </Button>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
