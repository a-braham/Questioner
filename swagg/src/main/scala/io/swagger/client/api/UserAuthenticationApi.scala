/**
 * Questioner API
 * Crowd-source questions for a meetup. Questioner helps the meetup organizer prioritize questions to be answered. Other users can vote on asked questions and they bubble to the top or bottom of the log.
 *
 * OpenAPI spec version: 1.0.0
 * Contact: kirumba.kamau@gmail.com
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 * Do not edit the class manually.
 */
package io.swagger.client.api

import io.swagger.client.model.Login
import io.swagger.client.model.Signup
import io.swagger.client.core._
import io.swagger.client.core.CollectionFormats._
import io.swagger.client.core.ApiKeyLocations._

object UserAuthenticationApi {

  /**
   * Login the user
   * 
   * Expected answers:
   *   code 200 : Seq[Login] (Successfully Logged in)
   *   code 400 :  (bad input parameters)
   * 
   * @param inventoryItem Inventory item to add
   */
  def authLoginPost(inventoryItem: Option[Login] = None): ApiRequest[Seq[Login]] =
    ApiRequest[Seq[Login]](ApiMethods.POST, "https://questioner-system.herokuapp.com/api/v2", "/auth/login", "application/json")
      .withBody(inventoryItem)
      .withSuccessResponse[Seq[Login]](200)
      .withErrorResponse[Unit](400)
        /**
   * By passing in the appropriate values, you can create an account 
   * 
   * Expected answers:
   *   code 201 : Seq[Signup] (Successfully saved)
   *   code 400 :  (bad input parameters)
   * 
   * @param inventoryItem Inventory item to add
   */
  def authSignupPost(inventoryItem: Option[Signup] = None): ApiRequest[Seq[Signup]] =
    ApiRequest[Seq[Signup]](ApiMethods.POST, "https://questioner-system.herokuapp.com/api/v2", "/auth/signup", "application/json")
      .withBody(inventoryItem)
      .withSuccessResponse[Seq[Signup]](201)
      .withErrorResponse[Unit](400)
      

}
