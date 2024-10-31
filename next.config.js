/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      // Rewrites for API calls to FastAPI during development vs. production
      {
        source: "/api/py/:path*",
        destination:
          process.env.NODE_ENV === "development"
            ? `${process.env.FASTAPI_DEV_URL}/:path*` // Use environment variable for local FastAPI
            : `${process.env.FASTAPI_PROD_URL}/api/py/:path*`, // Use environment variable for production FastAPI
      },
      // Rewrites for API documentation in FastAPI
      {
        source: "/docs",
        destination:
          process.env.NODE_ENV === "development"
            ? `${process.env.FASTAPI_DEV_URL}/docs` // FastAPI docs locally
            : `${process.env.FASTAPI_PROD_URL}/api/py/docs`, // Production FastAPI docs
      },
      // Rewrites for OpenAPI JSON schema in FastAPI
      {
        source: "/openapi.json",
        destination:
          process.env.NODE_ENV === "development"
            ? `${process.env.FASTAPI_DEV_URL}/openapi.json` // Local OpenAPI schema
            : `${process.env.FASTAPI_PROD_URL}/api/py/openapi.json`, // Production OpenAPI schema
      },
    ];
  },
};

module.exports = nextConfig;
