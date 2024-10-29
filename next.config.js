/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      // Rewrites for API calls to FastAPI during development vs. production
      {
        source: "/api/py/:path*",
        destination:
          process.env.NODE_ENV === "development"
            ? "http://127.0.0.1:8000/:path*" // Direct to FastAPI locally
            : "https://better-everyday-v3.vercel.app/api/py/:path*", // Adjust to production API path
      },
      // Rewrites for API documentation in FastAPI
      {
        source: "/docs",
        destination:
          process.env.NODE_ENV === "development"
            ? "http://127.0.0.1:8000/docs" // Direct to FastAPI docs locally
            : "https://better-everyday-v3.vercel.app/api/py/docs", // Production API docs
      },
      // Rewrites for OpenAPI JSON schema in FastAPI
      {
        source: "/openapi.json",
        destination:
          process.env.NODE_ENV === "development"
            ? "http://127.0.0.1:8000/openapi.json" // OpenAPI schema locally
            : "https://better-everyday-v3.vercel.app/api/py/openapi.json", // Production OpenAPI schema
      },
    ];
  },
};

module.exports = nextConfig;
