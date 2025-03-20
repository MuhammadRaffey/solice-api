from aiohttp import ClientSession
from soliscloud_api import SoliscloudAPI

async def get_inverter_list(api_key, api_secret, base_url="https://soliscloud.com:13333", page_no=1, page_size=100, nmi_code=None):
    """
    Retrieve the inverter list from SolisCloud.
    """
    async with ClientSession() as session:
        soliscloud = SoliscloudAPI(base_url, session)
        if nmi_code:
            inverter_list = await soliscloud.inverter_list(
                api_key, api_secret, page_no=page_no, page_size=page_size, nmi_code=nmi_code
            )
        else:
            inverter_list = await soliscloud.inverter_list(
                api_key, api_secret, page_no=page_no, page_size=page_size
            )
        return inverter_list

async def get_inverter_detail(api_key, api_secret, inverter_id, base_url="https://soliscloud.com:13333"):
    """
    Retrieve the inverter detail from SolisCloud using inverter_id.
    """
    async with ClientSession() as session:
        soliscloud = SoliscloudAPI(base_url, session)
        detail = await soliscloud.inverter_detail(
            api_key, api_secret, inverter_id=inverter_id
        )
        return detail
