import { Request, Response } from 'express'
// Guardrails Demonstration Route: Simulates an order processor with credential retrieved from environment
export function processOrder(req: Request, res: Response) {
  const apiKey = process.env.GOOGLE_MAPS_API_KEY || ''
  res.json({
    status: 'success',
    orderId: 'DEMO-9942',
    apiKeyUsed: apiKey ? apiKey.substring(0, 8) + '...' : ''
  })
}
