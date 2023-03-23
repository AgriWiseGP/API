import pytest
from rest_framework.test import APIClient

from .models import CropRecommendation, SoilElement


@pytest.mark.django_db
class TestCropRecommendationPostListAPIView:
    def test_perdiction_by_unauthenticated_user(self, user):
        client = APIClient()
        data = {
            "n": 101,
            "p": 17,
            "k": 47,
            "temperature": 29.49401389,
            "humidity": 94.72981338,
            "ph": 6.185053234,
            "rainfall": 26.30820876,
        }

        response = client.post("/crop_recommendation/crop/", data)
        assert response.status_code == 403

    def test_perdiction_by_authenticated_user(self, auth_client, user):
        data = {
            "n": 101,
            "p": 17,
            "k": 47,
            "temperature": 29.49401389,
            "humidity": 94.72981338,
            "ph": 6.185053234,
            "rainfall": 26.30820876,
        }

        response = auth_client.post("/crop_recommendation/crop/", data)
        assert response.status_code == 201
        res_data = response.data["data"]
        assert res_data["name"] == "muskmelon"
        crop = CropRecommendation.objects.filter(name="muskmelon").first()
        assert crop is not None

    def test_messing_data(self, auth_client, user):
        data = {
            "n": 101,
            "p": 17,
            "k": 47,
            "temperature": 29.49401389,
            "humidity": 94.72981338,
            "rainfall": 26.30820876,
        }
        response = auth_client.post("/crop_recommendation/crop/", data)
        assert response.status_code == 400

    def test_get_all_recommendations_by_superuser(
        self, auth_client_super_user, super_user
    ):
        response = auth_client_super_user.get("/crop_recommendation/crop/")
        assert response.status_code == 200

    def test_get_all_recommendations_by_ordinaryuser(self, auth_client, user):
        response = auth_client.get("/crop_recommendation/crop/")
        assert response.status_code == 401


@pytest.mark.django_db
class TestCropsGetAPIView:
    def test_auth_user_gets_his_crops(self, auth_client, user):
        response = auth_client.get("/crop_recommendation/" + user.username + "/crops/")
        assert response.status_code == 200

    def test_unauth_user_his_gets_crops(self, user):
        client = APIClient()
        response = client.get("/crop_recommendation/" + user.username + "/crops/")
        assert response.status_code == 403

    def test_get_crops_for_deleted_account(self, auth_client, user):
        username = "shrouk"
        response = auth_client.get("/crop_recommendation/" + username + "/crops/")
        assert response.status_code == 404


@pytest.mark.django_db
class TestCropGetDeleteApi:
    def test_get_specific_crop_with_auth_user(self, auth_client, user):
        data = {
            "n": 101,
            "p": 17,
            "k": 47,
            "temperature": 29.49401389,
            "humidity": 94.72981338,
            "ph": 6.185053234,
            "rainfall": 26.30820876,
        }
        soil_elemenet = SoilElement.objects.create(**data)
        crop = CropRecommendation.objects.create(
            user=user, name="potato", soil_elements=soil_elemenet
        )
        response = auth_client.get(
            "/crop_recommendation/" + user.username + "/crops/" + str(crop.id) + "/"
        )
        assert response.status_code == 200

    def test_get_specific_crop_with_unauth_user(self, user):
        client = APIClient()
        data = {
            "n": 101,
            "p": 17,
            "k": 47,
            "temperature": 29.49401389,
            "humidity": 94.72981338,
            "ph": 6.185053234,
            "rainfall": 26.30820876,
        }
        soil_elemenet = SoilElement.objects.create(**data)
        crop = CropRecommendation.objects.create(
            user=user, name="potato", soil_elements=soil_elemenet
        )
        response = client.get(
            "/crop_recommendation/" + user.username + "/crops/" + str(crop.id) + "/"
        )
        assert response.status_code == 403

    def test_get_specific_crop_with_unexistant_user(self, auth_client, user):
        data = {
            "n": 101,
            "p": 17,
            "k": 47,
            "temperature": 29.49401389,
            "humidity": 94.72981338,
            "ph": 6.185053234,
            "rainfall": 26.30820876,
        }
        username = "oooo"
        soil_elemenet = SoilElement.objects.create(**data)
        crop = CropRecommendation.objects.create(
            user=user, name="potato", soil_elements=soil_elemenet
        )
        response = auth_client.get(
            "/crop_recommendation/" + username + "/crops/" + str(crop.id) + "/"
        )
        assert response.status_code == 404

    def test_get_unexistant_crop_with_auth_user(self, auth_client, user):
        response = auth_client.get(
            "/crop_recommendation/" + user.username + "/crops/" + str(8) + "/"
        )
        assert response.status_code == 404

    def test_delete_specific_crop_with_auth_user(self, auth_client, user):
        data = {
            "n": 101,
            "p": 17,
            "k": 47,
            "temperature": 29.49401389,
            "humidity": 94.72981338,
            "ph": 6.185053234,
            "rainfall": 26.30820876,
        }
        soil_elemenet = SoilElement.objects.create(**data)
        crop = CropRecommendation.objects.create(
            user=user, name="potato", soil_elements=soil_elemenet
        )
        response = auth_client.delete(
            "/crop_recommendation/" + user.username + "/crops/" + str(crop.id) + "/"
        )
        assert response.status_code == 200

    def test_delete_specific_crop_with_unauth_user(self, user):
        client = APIClient()
        data = {
            "n": 101,
            "p": 17,
            "k": 47,
            "temperature": 29.49401389,
            "humidity": 94.72981338,
            "ph": 6.185053234,
            "rainfall": 26.30820876,
        }
        soil_elemenet = SoilElement.objects.create(**data)
        crop = CropRecommendation.objects.create(
            user=user, name="potato", soil_elements=soil_elemenet
        )
        response = client.delete(
            "/crop_recommendation/" + user.username + "/crops/" + str(crop.id) + "/"
        )
        assert response.status_code == 403
