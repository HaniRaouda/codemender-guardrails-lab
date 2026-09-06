import { Request, Response } from 'express'
// Guardrails Demonstration Route: Simulates an order processor with credential from environment variable
const GOOGLE_MAPS_API_KEY = process.env.GOOGLE_MAPS_API_KEY || ''
export function processOrder(req: Request, res: Response) {
  res.json({
    status: 'success',
    orderId: 'DEMO-9942',
    apiKeyUsed: GOOGLE_MAPS_API_KEY ? GOOGLE_MAPS_API_KEY.substring(0, 8) + '...' : ''
  })
}
