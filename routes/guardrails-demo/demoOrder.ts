import { Request, Response } from 'express'
// Guardrails Demonstration Route: Simulates an order processor with hardcoded credential
const GOOGLE_MAPS_API_KEY = 'AIzaSyD-mock-key-for-guardrails-demo-4402'
export function processOrder (req: Request, res: Response) {
  res.json({
    status: 'success',
    orderId: 'DEMO-9942',
    apiKeyUsed: GOOGLE_MAPS_API_KEY.substring(0, 8) + '...'
  })
}
