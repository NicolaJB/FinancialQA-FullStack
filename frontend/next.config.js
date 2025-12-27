/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,       // Enable strict mode for React
  output: 'export',            // Enable static export
  env: {
    // Public API URL, fallback to local if not set
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
  },
};

module.exports = nextConfig;
