
    def test_get_best_offer_checks_inventory(self, order):
        '''
        get the lowest price offer which has sufficient inventory
        '''
        best_offer = order.get_best_offer(self.supplier_offers)
        expected_best_offer = Offer(self.supplier_offers[0])
        self.assertEquals(
            best_offer.cost_price.value, expected_best_offer.cost_price.value)
        self.assertEquals(best_offer.supplier, expected_best_offer.supplier)


# appears in test output as:

esperanto.ordering.tests.main_tests
   GetBestOfferTests
      test_get_best_offer_accepts_equivalent_shipping_options ... ok
      get the lowest price offer which has sufficient inventory ... ok
      test_get_best_offer_retailer_wants_branding_but_no_supplier_can ... ok

