import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactCompiler: true,
  output: 'standalone',
  images: {
    unoptimized: true,
  },
  trailingSlash: true,
};

export default nextConfig;
