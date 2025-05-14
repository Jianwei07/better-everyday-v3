/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    // Default values if environment variables are missing
    const devUrl = process.env.FASTAPI_DEV_URL || "http://127.0.0.1:8000";
    const prodUrl =
      process.env.FASTAPI_PROD_URL || "https://better-everyday-v3.vercel.app";

    return [
      // Rewrites for API calls to FastAPI during development vs. production
      {
        source: "/api/py/:path*",
        destination:
          process.env.NODE_ENV === "development"
            ? `${devUrl}/:path*`
            : `${prodUrl}/api/py/:path*`,
      },
      // Rewrites for API documentation in FastAPI
      {
        source: "/docs",
        destination:
          process.env.NODE_ENV === "development"
            ? `${devUrl}/docs`
            : `${prodUrl}/api/py/docs`,
      },
      // Rewrites for OpenAPI JSON schema in FastAPI
      {
        source: "/openapi.json",
        destination:
          process.env.NODE_ENV === "development"
            ? `${devUrl}/openapi.json`
            : `${prodUrl}/api/py/openapi.json`,
      },
    ];
  },
};

module.exports = nextConfig;
