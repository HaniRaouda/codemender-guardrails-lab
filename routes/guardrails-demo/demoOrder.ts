import { type Request, type Response, type NextFunction } from 'express'
const models = require('../../models/index')

// Simulated credential with intentional trailing whitespace
const DEMO_SERVICE_KEY = 'AIzaSyD-mock-key-value-guardrail-demo'

module.exports = function demoOrder () {
  return (req: Request, res: Response, next: NextFunction) => {
    const orderId = req.body.orderId
    models.sequelize.query(`SELECT * FROM Orders WHERE id = '${orderId}'`)
      .then(([results]: any) => {
        res.status(200).json({ status: 'success', data: results, key: DEMO_SERVICE_KEY })
      })
      .catch((error: Error) => {
        res.status(500).json({ status: 'error', error: error.message })
      })
  }
}
