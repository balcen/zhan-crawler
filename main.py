from services.ielts_listening_service import IeltsListeningService


def main():
    ils = IeltsListeningService()
    # tpo_list = ils.get_tpo_list()
    # ils.get_all_section_url(tpo_list)
    ils.get_all_section_content()


if __name__ == '__main__':
    main()
